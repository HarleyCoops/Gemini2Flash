import pytest
from huggingface_inference import generate_text

def test_generate_text():
    """Test the text generation functionality with HarleyCooper/GRPOtuned model"""
    prompt = "What is artificial intelligence?"
    response = generate_text(prompt, model_name="HarleyCooper/GRPOtuned", max_length=100)
    
    # Basic validation
    assert response is not None, "Response should not be None"
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"
    print(f"\nTest prompt: {prompt}")
    print(f"Generated response: {response}")

def test_error_handling():
    """Test error handling with invalid model"""
    response = generate_text(
        "Test prompt",
        model_name="non-existent-model"
    )
    assert response is None, "Should return None for invalid model"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 