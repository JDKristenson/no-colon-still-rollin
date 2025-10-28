"""
PubMed research fetcher for No Colon, Still Rollin'
Fetches anti-cancer food research from PubMed/NCBI
"""
import time
from typing import List, Dict, Optional
from datetime import datetime
import re

try:
    from Bio import Entrez
except ImportError:
    print("⚠️  Biopython not installed. Run: pip install biopython")
    Entrez = None

from config import NCBI_EMAIL, NCBI_API_KEY, CANCER_SEARCH_TERMS
from database import Database


class PubMedFetcher:
    """Fetch and parse research from PubMed"""

    def __init__(self, email: str = NCBI_EMAIL, api_key: str = NCBI_API_KEY):
        if not Entrez:
            raise ImportError("Biopython required for PubMed access")

        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key

        self.db = Database()

    def search_pubmed(self, query: str, max_results: int = 50,
                      years: int = 10) -> List[str]:
        """
        Search PubMed and return list of PubMed IDs

        Args:
            query: Search query
            max_results: Maximum number of results
            years: How many years back to search

        Returns:
            List of PubMed IDs
        """
        print(f"🔍 Searching PubMed: {query}")

        # Add date filter for recent research
        date_filter = f" AND {datetime.now().year - years}[PDAT]:{datetime.now().year}[PDAT]"
        full_query = query + date_filter

        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=full_query,
                retmax=max_results,
                sort="relevance"
            )
            record = Entrez.read(handle)
            handle.close()

            pmids = record.get("IdList", [])
            print(f"  Found {len(pmids)} articles")
            return pmids

        except Exception as e:
            print(f"  ❌ Error searching: {e}")
            return []

    def fetch_article_details(self, pmid: str) -> Optional[Dict]:
        """
        Fetch detailed information about an article

        Args:
            pmid: PubMed ID

        Returns:
            Dictionary with article details
        """
        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=pmid,
                rettype="medline",
                retmode="xml"
            )
            records = Entrez.read(handle)
            handle.close()

            if not records.get("PubmedArticle"):
                return None

            article = records["PubmedArticle"][0]
            medline = article.get("MedlineCitation", {})
            pubmed_data = article.get("PubmedData", {})

            # Extract basic info
            article_data = medline.get("Article", {})
            title = article_data.get("ArticleTitle", "")
            abstract_parts = article_data.get("Abstract", {}).get("AbstractText", [])

            # Handle abstract (can be list or string)
            if isinstance(abstract_parts, list):
                abstract = " ".join(str(part) for part in abstract_parts)
            else:
                abstract = str(abstract_parts)

            # Authors
            authors_list = article_data.get("AuthorList", [])
            authors = ", ".join(
                f"{a.get('LastName', '')} {a.get('Initials', '')}"
                for a in authors_list[:3]  # First 3 authors
            )
            if len(authors_list) > 3:
                authors += " et al."

            # Journal
            journal = article_data.get("Journal", {})
            journal_title = journal.get("Title", "")

            # Year
            pub_date = journal.get("JournalIssue", {}).get("PubDate", {})
            year = pub_date.get("Year", "")
            if not year:
                # Try MedlineDate
                medline_date = pub_date.get("MedlineDate", "")
                year_match = re.search(r"\d{4}", medline_date)
                year = year_match.group(0) if year_match else ""

            # DOI
            doi = ""
            for id_data in pubmed_data.get("ArticleIdList", []):
                if id_data.attributes.get("IdType") == "doi":
                    doi = str(id_data)
                    break

            return {
                "pubmed_id": pmid,
                "title": title,
                "authors": authors,
                "journal": journal_title,
                "year": int(year) if year else None,
                "abstract": abstract,
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            }

        except Exception as e:
            print(f"  ❌ Error fetching article {pmid}: {e}")
            return None

    def extract_dosing_info(self, abstract: str) -> Dict:
        """
        Extract dosing information from abstract using pattern matching

        Args:
            abstract: Article abstract text

        Returns:
            Dictionary with dose_amount, dose_unit, etc.
        """
        dosing_info = {
            "dose_amount": None,
            "dose_unit": "",
            "dose_frequency": "",
            "subject_weight_kg": None,
        }

        # Common patterns for dosing
        # e.g., "100 mg/kg", "5 g daily", "500 mg twice daily"
        dose_pattern = r"(\d+\.?\d*)\s*(mg|g|μg|ug|mcg|ml)(?:/kg)?(?:\s+(?:per|/)?\s*(?:day|daily|twice|three times))?"
        matches = re.findall(dose_pattern, abstract.lower())

        if matches:
            amount, unit = matches[0][:2]
            dosing_info["dose_amount"] = float(amount)
            dosing_info["dose_unit"] = unit

            # Check for frequency
            if "twice" in abstract.lower():
                dosing_info["dose_frequency"] = "twice daily"
            elif "three times" in abstract.lower():
                dosing_info["dose_frequency"] = "three times daily"
            elif "daily" in abstract.lower() or "per day" in abstract.lower():
                dosing_info["dose_frequency"] = "daily"

        # Look for subject weights (mice are usually 20-30g)
        weight_pattern = r"(\d+)\s*g\s+(?:mice|mouse|rats?)"
        weight_match = re.search(weight_pattern, abstract.lower())
        if weight_match:
            weight_g = float(weight_match.group(1))
            dosing_info["subject_weight_kg"] = weight_g / 1000

        return dosing_info

    def classify_study_type(self, abstract: str, title: str) -> str:
        """
        Determine study type from abstract/title

        Args:
            abstract: Article abstract
            title: Article title

        Returns:
            Study type (in_vitro, animal, human_observational, etc.)
        """
        text = (abstract + " " + title).lower()

        if any(term in text for term in ["clinical trial", "randomized", "placebo"]):
            return "human_clinical"
        elif any(term in text for term in ["meta-analysis", "systematic review"]):
            return "meta_analysis"
        elif any(term in text for term in ["cohort", "case-control", "observational", "epidemiologic"]):
            return "human_observational"
        elif any(term in text for term in ["mice", "mouse", "rats", "rat", "animal"]):
            return "animal"
        elif any(term in text for term in ["in vitro", "cell line", "cell culture", "petri"]):
            return "in_vitro"
        else:
            return "in_vitro"  # Default

    def extract_food_and_compound(self, title: str, abstract: str) -> tuple:
        """
        Extract food/compound being studied

        Returns:
            (food_name, compound_name)
        """
        text = (title + " " + abstract).lower()

        # Common foods and their compounds
        food_compounds = {
            "ginger": ["gingerol", "shogaol", "zingerone"],
            "garlic": ["allicin", "alliin", "s-allyl cysteine"],
            "turmeric": ["curcumin", "curcuminoid"],
            "broccoli": ["sulforaphane", "glucosinolate", "isothiocyanate"],
            "cauliflower": ["sulforaphane", "glucosinolate"],
            "kale": ["sulforaphane", "glucosinolate"],
            "brussels sprouts": ["sulforaphane", "glucosinolate"],
            "green tea": ["egcg", "catechin", "epigallocatechin"],
            "berries": ["anthocyanin", "ellagic acid"],
            "fish oil": ["omega-3", "epa", "dha"],
        }

        found_food = None
        found_compound = None

        for food, compounds in food_compounds.items():
            if food in text:
                found_food = food
                for compound in compounds:
                    if compound in text:
                        found_compound = compound
                        break
                break

        return found_food, found_compound

    def update_research_database(self, search_terms: List[str] = None,
                                 max_per_search: int = 20):
        """
        Update database with latest research

        Args:
            search_terms: List of search queries (default: from config)
            max_per_search: Max results per search term
        """
        if search_terms is None:
            search_terms = CANCER_SEARCH_TERMS

        print("🔬 Updating research database from PubMed...\n")
        total_added = 0
        total_skipped = 0

        for search_term in search_terms:
            # Search PubMed
            pmids = self.search_pubmed(search_term, max_results=max_per_search)

            for pmid in pmids:
                # Check if already in database
                existing = self.db.conn.execute(
                    "SELECT id FROM research_studies WHERE pubmed_id = ?",
                    (pmid,)
                ).fetchone()

                if existing:
                    total_skipped += 1
                    continue

                # Fetch article details
                article = self.fetch_article_details(pmid)
                if not article:
                    continue

                # Extract additional info
                dosing_info = self.extract_dosing_info(article["abstract"])
                study_type = self.classify_study_type(article["abstract"], article["title"])
                food, compound = self.extract_food_and_compound(article["title"], article["abstract"])

                # Determine cancer type
                cancer_type = "general"
                text_lower = (article["title"] + " " + article["abstract"]).lower()
                if "colon" in text_lower or "colorectal" in text_lower:
                    cancer_type = "colon"
                elif "breast" in text_lower:
                    cancer_type = "breast"
                elif "prostate" in text_lower:
                    cancer_type = "prostate"
                elif "lung" in text_lower:
                    cancer_type = "lung"

                # Save to database
                study_data = {
                    **article,
                    **dosing_info,
                    "study_type": study_type,
                    "food_studied": food or "",
                    "compound_studied": compound or "",
                    "cancer_type": cancer_type,
                }

                result = self.db.add_research_study(study_data)
                if result > 0:
                    print(f"  ✅ Added: {article['title'][:60]}...")
                    total_added += 1
                else:
                    total_skipped += 1

                # Be nice to NCBI servers
                time.sleep(0.5 if NCBI_API_KEY else 1)

            print()  # Blank line between search terms

        print(f"\n✅ Research update complete!")
        print(f"   Added: {total_added} new studies")
        print(f"   Skipped: {total_skipped} existing studies")

    def get_research_summary(self) -> Dict:
        """Get summary statistics of research database"""
        cursor = self.db.conn.cursor()

        # Total studies
        cursor.execute("SELECT COUNT(*) FROM research_studies")
        total = cursor.fetchone()[0]

        # By study type
        cursor.execute("""
            SELECT study_type, COUNT(*)
            FROM research_studies
            GROUP BY study_type
        """)
        by_type = dict(cursor.fetchall())

        # By cancer type
        cursor.execute("""
            SELECT cancer_type, COUNT(*)
            FROM research_studies
            GROUP BY cancer_type
        """)
        by_cancer = dict(cursor.fetchall())

        # Most studied foods
        cursor.execute("""
            SELECT food_studied, COUNT(*)
            FROM research_studies
            WHERE food_studied != ''
            GROUP BY food_studied
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        top_foods = dict(cursor.fetchall())

        return {
            "total_studies": total,
            "by_study_type": by_type,
            "by_cancer_type": by_cancer,
            "top_foods": top_foods,
        }


if __name__ == "__main__":
    # Test the fetcher
    fetcher = PubMedFetcher()

    print("Testing PubMed fetcher...\n")
    print("=" * 60)

    # Update research
    fetcher.update_research_database(max_per_search=5)

    # Show summary
    print("\n" + "=" * 60)
    print("Research Database Summary:")
    print("=" * 60)
    summary = fetcher.get_research_summary()
    print(f"Total studies: {summary['total_studies']}")
    print(f"\nBy study type:")
    for study_type, count in summary['by_study_type'].items():
        print(f"  {study_type}: {count}")
    print(f"\nBy cancer type:")
    for cancer_type, count in summary['by_cancer_type'].items():
        print(f"  {cancer_type}: {count}")
    print(f"\nTop studied foods:")
    for food, count in summary['top_foods'].items():
        print(f"  {food}: {count} studies")
