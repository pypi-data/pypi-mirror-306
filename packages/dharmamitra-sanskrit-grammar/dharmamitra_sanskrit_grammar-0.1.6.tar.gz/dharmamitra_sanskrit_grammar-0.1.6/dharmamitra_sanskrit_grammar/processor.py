import requests
from typing import List, Dict, Union

class DharmamitraSanskritProcessor:
    """
    Process batches of Sanskrit sentences using the Dharmamitra API.
    """
    
    MODES = {
        'unsandhied',
        'lemma',
        'unsandhied-lemma-morphosyntax'
    }
    
    OUTPUT_FORMATS = {'dict', 'string'}
    
    def __init__(self, api_url: str = 'https://dharmamitra.org/api/tagging/'):
        """
        Initialize the processor with the API endpoint.
        
        Args:
            api_url: The Dharmamitra API endpoint URL
        """
        self.api_url = api_url
        self._headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'Basic b2xkc3R1ZGVudDpiZWhhcHB5',
            'Connection': 'keep-alive',
            'Origin': 'https://dharmamitra.org',
            'Referer': 'https://dharmamitra.org/rnd',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
    
    def process_batch(
        self,
        sentences: List[str],
        mode: str = "lemma",
        human_readable_tags: bool = True,
        output_format: str = "dict"
    ) -> Union[List[Dict], List[str]]:
        """
        Process a batch of Sanskrit sentences.
        
        Args:
            sentences: List of Sanskrit sentences to process
            mode: Analysis mode ('lemma', 'unsandhied', 'unsandhied-morphosyntax',
                  'lemma-morphosyntax', 'unsandhied-lemma-morphosyntax')
            human_readable_tags: Whether to return human-readable tags
            output_format: Format of the output ('dict' or 'string')
            
        Returns:
            If output_format is 'dict': List of dictionaries containing the grammatical analysis
            If output_format is 'string': List of strings containing concatenated unsandhied values
            
        Raises:
            ValueError: If an invalid mode or output format is specified
            requests.exceptions.RequestException: If the API request fails
        """
        if mode not in self.MODES:
            raise ValueError(
                f"Invalid mode: {mode}. Must be one of: {', '.join(self.MODES)}"
            )
            
        if output_format not in self.OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format: {output_format}. Must be one of: {', '.join(self.OUTPUT_FORMATS)}"
            )
            
        data = {
            "input_sentence": "\n".join(sentences),
            "mode": mode,
            "input_encoding": "auto",
            "human_readable_tags": human_readable_tags
        }
        
        try:
            response = requests.post(self.api_url, headers=self._headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if output_format == "string":
                field = "unsandhied" if mode == "unsandhied" else "lemma"
                return [
                    " ".join(
                        word[field]
                        for word in sentence['grammatical_analysis']
                        if word[field]
                    )
                    for sentence in result
                ]
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"API request failed for mode '{mode}': {str(e)}"
            )

input_sentences = ["yeṣāṃ saṃsiddhiḥ", "tatra saṃsiddhiḥ"]

processor = DharmamitraSanskritProcessor()
results = processor.process_batch(input_sentences, mode="lemma", output_format="string")
print(results)  # Output: ['yeṣa saṃsiddhiḥ', 'tatra saṃsiddhiḥ']