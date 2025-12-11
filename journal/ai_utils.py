import google.generativeai as genai
from django.conf import settings

def check_grammar(text):
    """
    Uses Gemini AI to check grammar and grammar correction.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        return {'error': 'Gemini API Key not configured'}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Act as a professional editor. Correct the grammar and spelling of the following text.
        Return ONLY the corrected text. If the text is already correct, return it as is.
        
        Text:
        {text}
        """
        
        response = model.generate_content(prompt)
        corrected_text = response.text.strip()
        
        return {'corrected': corrected_text}
    except Exception as e:
        return {'error': str(e)}
