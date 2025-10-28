"""
PubMed API client for fetching cancer research studies
"""
import requests
from typing import List, Dict, Optional
from config import NCBI_EMAIL, NCBI_API_KEY


class PubMedClient:
    """Client for interacting with NCBI PubMed API"""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email: str = NCBI_EMAIL, api_key: str = NCBI_API_KEY):
        self.email = email
        self.api_key = api_key

    def search_studies(self, query: str, max_results: int = 20) -> List[str]:
        """
        Search PubMed and return list of PubMed IDs

        Args:
            query: Search query (e.g., "ginger AND colon cancer")
            max_results: Maximum number of results to return

        Returns:
            List of PubMed IDs
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': 'relevance',
            'email': self.email,
        }

        if self.api_key:
            params['api_key'] = self.api_key

        try:
            response = requests.get(f"{self.BASE_URL}/esearch.fcgi", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return data.get('esearchresult', {}).get('idlist', [])
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []

    def fetch_study_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for given PubMed IDs

        Args:
            pubmed_ids: List of PubMed IDs to fetch

        Returns:
            List of study details dictionaries
        """
        if not pubmed_ids:
            return []

        params = {
            'db': 'pubmed',
            'id': ','.join(pubmed_ids),
            'retmode': 'xml',
            'email': self.email,
        }

        if self.api_key:
            params['api_key'] = self.api_key

        try:
            response = requests.get(f"{self.BASE_URL}/efetch.fcgi", params=params, timeout=30)
            response.raise_for_status()

            # Parse XML response
            studies = self._parse_pubmed_xml(response.text)
            return studies
        except Exception as e:
            print(f"Error fetching PubMed details: {e}")
            return []

    def search_and_fetch(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Convenience method to search and fetch study details in one call

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of study details
        """
        pubmed_ids = self.search_studies(query, max_results)
        if not pubmed_ids:
            return []
        return self.fetch_study_details(pubmed_ids)

    def _parse_pubmed_xml(self, xml_text: str) -> List[Dict]:
        """
        Parse PubMed XML response into structured data

        Args:
            xml_text: XML response from PubMed

        Returns:
            List of parsed study dictionaries
        """
        import xml.etree.ElementTree as ET

        studies = []
        try:
            root = ET.fromstring(xml_text)

            for article in root.findall('.//PubmedArticle'):
                study = {}

                # PubMed ID
                pmid = article.find('.//PMID')
                if pmid is not None:
                    study['pubmed_id'] = pmid.text

                # Title
                title = article.find('.//ArticleTitle')
                if title is not None:
                    study['title'] = title.text or ""

                # Abstract
                abstract_parts = article.findall('.//AbstractText')
                if abstract_parts:
                    abstract = ' '.join([a.text or "" for a in abstract_parts])
                    study['abstract'] = abstract
                else:
                    study['abstract'] = ""

                # Authors
                authors = article.findall('.//Author')
                author_list = []
                for author in authors[:5]:  # First 5 authors
                    last = author.find('.//LastName')
                    first = author.find('.//ForeName')
                    if last is not None:
                        name = last.text or ""
                        if first is not None:
                            name = f"{first.text} {name}"
                        author_list.append(name)
                study['authors'] = ', '.join(author_list) if author_list else ""

                # Journal
                journal = article.find('.//Journal/Title')
                if journal is not None:
                    study['journal'] = journal.text or ""
                else:
                    study['journal'] = ""

                # Year
                year = article.find('.//PubDate/Year')
                if year is not None:
                    try:
                        study['year'] = int(year.text)
                    except:
                        study['year'] = None
                else:
                    study['year'] = None

                # DOI
                doi_elem = article.find('.//ArticleId[@IdType="doi"]')
                if doi_elem is not None:
                    study['doi'] = doi_elem.text
                else:
                    study['doi'] = ""

                # URL
                if study.get('pubmed_id'):
                    study['url'] = f"https://pubmed.ncbi.nlm.nih.gov/{study['pubmed_id']}/"
                else:
                    study['url'] = ""

                studies.append(study)

        except Exception as e:
            print(f"Error parsing PubMed XML: {e}")

        return studies
