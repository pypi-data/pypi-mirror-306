# llmjudge/core.py

def evaluate(model_output, reference_output):
    """
    Evaluates the language model output against a reference output.

    Parameters:
        model_output (str): The output from the language model.
        reference_output (str): The expected reference output.

    Returns:
        float: An evaluation score between 0 and 1.
    """
    # Simple example comparing the outputs
    score = 1.0 if model_output == reference_output else 0.0
    return score
