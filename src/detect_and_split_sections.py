import json
from typing import List, Dict

def refine_sections(input_list: str, llm) -> List[Dict]:
    """
    Refine sections by filtering out figures, tables, and fragments.
    Uses local filtering instead of LLM to avoid rate limits.
    """
    try:
        # Parse the input JSON
        sections = json.loads(input_list) if isinstance(input_list, str) else input_list
        
        # Filter out unwanted sections locally
        refined = []
        for item in sections:
            section_name = item.get("section", "").lower()
            
            # Skip figures and tables
            if section_name.startswith("figure") or section_name.startswith("table"):
                continue
            
            # Skip very short or meaningless sections
            if len(section_name) < 3:
                continue
                
            # Skip fragments (sections with less than 2 words)
            if len(section_name.split()) < 2 and section_name not in ["abstract", "introduction", "conclusion", "references", "acknowledgments", "appendix"]:
                continue
            
            refined.append(item)
        
        return refined
        
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print("Warning: Could not parse sections. Returning empty list.")
        print("Error:", e)
        return []


def split_sections_with_content(text: str, detected_sections: List[Dict]) -> List[Dict]:
    """
    Split text into sections/subsections using detected start positions.
    Returns a list of dicts with: section, subsection (if any), start, content.
    """
    if not detected_sections:
        return {"Full_Paper" : text}

    # Sort by start index to ensure correct order
    detected_sections = sorted(detected_sections, key=lambda x: x["start"])
    results = {}

    for i, sec in enumerate(detected_sections):
        start = sec["start"]
        end = detected_sections[i + 1]["start"] if i + 1 < len(detected_sections) else len(text)

        # Section details
        section_name = sec["section"]
        subsection_name = sec.get("subsection", None)
        section_text = text[start:end].strip()

        results[section_name] = section_text

        if subsection_name:
            results[subsection_name] = results.pop(section_name)

    return results