import os
import json
import google.generativeai as genai

def get_gemini_client():
    """
    Lazy initialization for safety, preventing startup errors if API key is missing.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        return genai
    except Exception as e:
        print(f"Failed to initialize Google Gen AI: {e}")
        return None

def suggest_dynamic_fields(prompt, city_context="Cotonou"):
    """
    AI-powered questionnaire generation: Takes a client's free-form business need
    and returns a structured JSON questionnaire ready for agent collection.
    """
    client = get_gemini_client()
    if not client:
        return {
            "title": f"Collecte: {prompt[:30]}...",
            "description": f"Enquête intelligente générée pour {city_context}",
            "zone": {
                "type": "city",
                "name": city_context,
                "lat": 6.3654,
                "lng": 2.4183,
                "radiusKm": 5.0
            },
            "totalRequired": 10,
            "budgetAgentFcfa": 1200,
            "fields": [
                {"id": "f1", "type": "text", "label": "Nom de la boutique", "required": True},
                {"id": "f2", "type": "number", "label": "Prix (FCFA)", "required": True},
                {"id": "f3", "type": "select", "label": "Disponibilité", "required": True, "options": ["Disponible", "Rupture"]},
                {"id": "f4", "type": "photo", "label": "Photo", "required": True},
                {"id": "f5", "type": "gps", "label": "GPS", "required": True}
            ]
        }
    
    try:
        system_instruction = (
            "Tu es DataBroker229 IA. Génère des questionnaires d'enquête pour le Bénin. "
            "Réponds UNIQUEMENT avec du JSON valide, sans texte supplémentaire."
        )
        
        user_prompt = f"""Génère un questionnaire pour: {prompt}
        Zone: {city_context}
        
        Réponds avec JSON: {{title, description, zone: {{type, name, lat, lng, radiusKm}}, totalRequired, budgetAgentFcfa, fields: [...]}}
        """
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_prompt, system_instruction=system_instruction)
        
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        parsed = json.loads(response_text.strip())
        return parsed
    
    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            "title": f"Collecte: {prompt[:30]}...",
            "description": f"Enquête pour {city_context}",
            "zone": {"type": "city", "name": city_context, "lat": 6.3654, "lng": 2.4183, "radiusKm": 5.0},
            "totalRequired": 10,
            "budgetAgentFcfa": 1200,
            "fields": [
                {"id": "f1", "type": "text", "label": "Nom", "required": True},
                {"id": "f2", "type": "number", "label": "Prix", "required": True},
                {"id": "f3", "type": "select", "label": "Disponibilité", "required": True, "options": ["Oui", "Non"]},
                {"id": "f4", "type": "photo", "label": "Photo", "required": True},
                {"id": "f5", "type": "gps", "label": "GPS", "required": True}
            ]
        }

def chat_helper_reply(user_message, conversation_history=None):
    """
    Chatbot endpoint: Provides real-time AI assistance to platform users.
    """
    if conversation_history is None:
        conversation_history = []
    
    client = get_gemini_client()
    if not client:
        return {
            "reply": "L'assistant IA n'est pas disponible. Contactez-nous sur WhatsApp.",
            "whatsapp_link": "https://wa.me/22955256871"
        }
    
    try:
        system_instruction = (
            "Tu es l'assistant IA de DataBroker229. "
            "Aide les utilisateurs avec professionnel et amitié. "
            "Réponds en français béninois simple."
        )
        
        messages = []
        for msg in conversation_history:
            messages.append({"role": msg.get("role", "user"), "parts": [msg.get("content", "")]})
        
        messages.append({"role": "user", "parts": [user_message]})
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=messages[:-1])
        response = chat.send_message(user_message)
        
        reply_text = response.text
        needs_whatsapp = any(kw in reply_text.lower() for kw in ["whatsapp", "contact", "support"])
        
        return {
            "reply": reply_text,
            "whatsapp_link": "https://wa.me/22955256871" if needs_whatsapp else None
        }
    
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "reply": "Erreur. Contactez notre équipe via WhatsApp.",
            "whatsapp_link": "https://wa.me/22955256871"
        }
