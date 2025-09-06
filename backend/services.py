import time

class MockLLMService:
    """
    A mock service that simulates calling a Large Language Model (LLM)
    to get a diagnosis for a given text.
    """
    def get_diagnosis(self, text: str) -> str:
        """
        Simulates the LLM processing time and returns a hardcoded diagnosis.
        """
        print(f"Simulating LLM call for text: '{text}'...")
        time.sleep(1) # Simulate network latency and processing time

        # In a real application, this would be a call to an LLM API.
        # The logic could be much more complex, involving prompt engineering.
        if "yellow" in text.lower():
            return "The crop shows signs of nitrogen deficiency. Recommendation: Apply a nitrogen-rich fertilizer."
        elif "spots" in text.lower():
            return "The crop may have a fungal infection. Recommendation: Apply a broad-spectrum fungicide."
        else:
            return "Could not determine the issue from the text. Please provide a photo for more accurate diagnosis."

class MockActionService:
    """
    A mock service that simulates performing external actions, such as sending
    a WhatsApp message or triggering an IoT device.
    """
    def send_whatsapp_message(self, farmer_id: str, message: str) -> dict:
        """
        Simulates sending a message to the farmer via WhatsApp.
        """
        print(f"--- SIMULATING ACTION ---")
        print(f"To: {farmer_id}")
        print(f"Message: {message}")
        print(f"-------------------------")
        # In a real application, this would call the WhatsApp Cloud API.
        return {"status": "success", "recipient": farmer_id, "message_id": f"fake_msg_{int(time.time())}"}

# Create singleton instances of the services to be used in the app.
llm_service = MockLLMService()
action_service = MockActionService()
