"""Parser for Signatera ctDNA variant information Excel files"""
import openpyxl
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def parse_signatera_excel(file_path: str) -> List[Dict]:
    """
    Parse Signatera Excel file and return list of marker dictionaries.
    
    Expected format:
    - Column A: position (integer)
    - Column B: chromosome (string, e.g., "chr16")
    - Column C: type ("Transversion" or "Transition")
    - Column D: ref (reference base: A, C, G, T)
    - Column E: mut (mutation base: A, C, G, T)
    - Column F: targetId (e.g., "target_1")
    
    Returns:
        List of dicts with keys: target_id, chromosome, position, variant_type, ref_base, mut_base
    """
    try:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        
        markers = []
        
        # Skip header row (row 1)
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                # Extract values
                position = row[0]  # Column A
                chromosome = row[1]  # Column B
                variant_type = row[2]  # Column C
                ref_base = row[3]  # Column D
                mut_base = row[4]  # Column E
                target_id = row[5]  # Column F
                
                # Validate required fields
                if not all([position, chromosome, variant_type, ref_base, mut_base, target_id]):
                    logger.warning(f"Row {row_idx} has missing data, skipping")
                    continue
                
                # Validate chromosome format
                if not str(chromosome).startswith('chr'):
                    logger.warning(f"Row {row_idx}: Invalid chromosome format: {chromosome}")
                    continue
                
                # Validate variant type
                if variant_type not in ["Transversion", "Transition"]:
                    logger.warning(f"Row {row_idx}: Invalid variant type: {variant_type}")
                    continue
                
                # Validate bases
                valid_bases = ['A', 'C', 'G', 'T']
                if ref_base not in valid_bases or mut_base not in valid_bases:
                    logger.warning(f"Row {row_idx}: Invalid base(s): ref={ref_base}, mut={mut_base}")
                    continue
                
                marker = {
                    "target_id": str(target_id),
                    "chromosome": str(chromosome),
                    "position": int(position),
                    "variant_type": str(variant_type),
                    "ref_base": str(ref_base),
                    "mut_base": str(mut_base),
                }
                
                markers.append(marker)
                
            except (ValueError, TypeError, IndexError) as e:
                logger.error(f"Error parsing row {row_idx}: {e}")
                continue
        
        logger.info(f"Parsed {len(markers)} markers from {file_path}")
        return markers
        
    except Exception as e:
        logger.error(f"Failed to parse Signatera file {file_path}: {e}", exc_info=True)
        raise ValueError(f"Failed to parse Signatera Excel file: {str(e)}")

