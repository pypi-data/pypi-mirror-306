import regex as re

def sentence_count(text: str) -> int:
    """
    Returns the number of sentences in the text string.
    
    This function identifies sentences and accounts for
    several common abbreviations but not all abbreviations.
    
    Parameters:
    text (str): The input text
    
    Returns:
    int: The number of sentences in the input text.
    """
    common_abbrv = [
        "Mr.", "Mrs.", "Dr.", "Jr.", "Sr.", "Ms.", "Prof.", "Rev.", "St.", "Sgt.", "Gen.",
        "Lt.", "Col.", "Maj.", "Capt.", "Adm.", "Hon.", "Pres.", "Gov.", "Sen.", "Rep.",
        "Supt.", "Det.", "Cmdr.", "Sec.", "Amb.", "Asst.", "Dir.", "Mgr.", "Op.", "Opr.",
        "PhD.", "M.D.", "D.D.S.", "D.O.", "R.N.", "LLC.", "Inc.", "Ltd.", "Corp.", "Co.",
        "etc.", "e.g.", "i.e.", "viz.", "a.k.a.", "U.S.", "U.K.", "U.N.", "U.A.E.", "E.U.",
        "B.C.", "A.D.", "a.m.", "p.m.", "No.", "Jan.", "Feb.", "Mar.", "Apr.", "Jun.", "Jul.",
        "Aug.", "Sep.", "Sept.", "Oct.", "Nov.", "Dec.", "Mt.", "Ft.", "Blvd.", "Rd.",
        "Ln.", "Ct.", "Pl.", "Sq.", "Dr.", "Cir.", "Pkwy.", "Hwy.", "Ste.", "Dept.", "Univ.",
        "Hosp.", "Intl.", "Natl.", "Assoc.", "Dept.", "Div.", "No.", "Vol.", "Ed."
    ]
    
    abbrv_pattern = '|'.join(common_abbrv)
    
    sentences = re.split(rf'(?<!\b(?:{abbrv_pattern}))'r'(?<!\b\w\.\w\.)'r'(?<!\b\w\.\b)'r'(?<!\.\.)'r'(?<=[.!?])\s+', text.strip(), flags=re.IGNORECASE)
    identified_sentences = [s for s in sentences if s!= ""]
    
    return len(identified_sentences)
