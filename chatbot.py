import speech_recognition as sr
from typing import Dict
import pyttsx3

class FSAChatbot:
    def __init__(self, fsa_data: Dict):
        self.fsa_data = fsa_data
        self.rules = self._create_rules()
        self.engine = pyttsx3.init()  # Initialize the text-to-speech engine
        self.recognizer = sr.Recognizer()  # Initialize the speech recognizer
        self.microphone = sr.Microphone()  # Initialize the microphone

        self.engine.setProperty('rate', 120)
        
    def _create_rules(self) -> Dict:
        """
        Create predefined rules for the chatbot based on FSA data.
        """
        rules = {
            "states": self.fsa_data["states"],
            "transitions": self.fsa_data["transitions"],
            "initial_state": None,
            "final_state": None,
            "input_symbols": set()
        }
        
        # Identify initial and final states
        for state in rules["states"]:
            if "Initial" in state["type"]:
                rules["initial_state"] = state
            if "Final" in state["type"]:
                rules["final_state"] = state
        
        # Collect input symbols from transitions
        for transition in rules["transitions"]:
            rules["input_symbols"].add(transition["label"])
        
        return rules

    def speak(self, text: str):
 
  
        self.engine.stop()  # Stop any current speech
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
   
      try:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
            self.speak("Please ask your question now")
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
        question = self.recognizer.recognize_google(audio)
        print(f"You asked: {question}")
        return question.lower()
      except sr.WaitTimeoutError:
        self.speak("I didn't hear anything. Please try again.")
        return ""
      except sr.UnknownValueError:
        self.speak("Sorry, I couldn't understand your question. Please try again.")
        return ""
      except sr.RequestError:
        self.speak("Sorry, there was an error with the speech recognition service.")
        return ""
      except Exception as e:
        print(f"Error in listening: {str(e)}")
        return ""

    def answer_question(self, question: str) -> str:
        """
        Answer questions based on predefined rules and provide voice output.
        """
        if not question:
            return "No question detected."
            
        question = question.lower()
        
        # Rule 1: What are the states in the given FSA?
        if "states" in question and ("what" in question or "list" in question):
            def sort_key(state):
                if 'final' in state['type']:
                    return 0  # Final states come first
                elif 'normal' in state['type']:
                    return 1  # Normal states come second
                elif 'initial' in state['type']:
                    return 2  # Initial states come last
                else:
                    return 3  # Any other type (if exists)

            sorted_states = sorted(self.rules["states"], key=sort_key)
            states = [f"State {state['id']} ({', '.join(state['type'])})" 
                      for state in sorted_states]
            response = f"The states in the FSA are: {', '.join(states)}."
        
        # Rule 2: What are the transitions in the given FSA?
        elif "transitions" in question or "transitions" in question:  # Handling possible mispronunciation
            transitions = [f"State {t['source']} -> State {t['destination']} (Input: '{t['label']}')" 
                          for t in self.rules["transitions"]]
            response = f"The transitions in the FSA are: {', '.join(transitions)}."
        
        # Rule 3: What is the initial state?
        elif "initial state" in question or "initial" in question:
            if self.rules["initial_state"]:
                response = f"The initial state is State {self.rules['initial_state']['id']}."
            else:
                response = "No initial state detected."
        
        # Rule 4: What is the final state?
        elif "final state" in question or "final" in question:
            if self.rules["final_state"]:
                response = f"The final state is State {self.rules['final_state']['id']}."
            else:
                response = "No final state detected."
        
        # Rule 5: What is the input symbol for the transition from state X to state Y?
        elif ("input symbol" in question or "input" in question) and ("transition" in question or "from" in question):
            try:
                # Extract numbers from the question that might be state IDs
                numbers = [int(s) for s in question.split() if s.isdigit()]
                
                if len(numbers) >= 2:
                    source = numbers[0]
                    dest = numbers[1]
                    
                    # Search for the transition in the rules
                    for t in self.rules["transitions"]:
                        if t["source"] == source and t["destination"] == dest:
                            response = f"The input symbol for the transition from State {source} to State {dest} is '{t['label']}'."
                            break
                    else:
                        response = f"No transition found from State {source} to State {dest}."
                else:
                    response = "Please specify both the source and destination states in your question."
            except:
                response = "Sorry, I couldn't understand the states in your question. Please try asking again."
        
        # Rule 6: Basic conceptual questions about FSA
        elif "what is a finite state automata" in question or "what is an fsa" in question or "what is the finite state automata" in question:
            response = ("A Finite State Automaton (FSA) is a mathematical model of computation used to "
                        "design both computer programs and sequential logic circuits. It consists of a "
                        "finite number of states, transitions between these states, and actions.")
        
        elif "what is a state" in question:
            response = ("A state is a condition or situation of the FSA at a given time. It represents "
                        "a specific configuration of the system.")
        
        elif "what is a transition" in question:
            response = ("A transition is a change from one state to another in response to an input symbol.")
        
        elif "what is an input symbol" in question or "what are input symbols" in question:
            response = ("An input symbol is a character or token that triggers a transition between states "
                        "in an FSA.")
        
        # Default response
        else:
            response = "Sorry, I don't understand that question. Please ask about the FSA states, transitions, or basic concepts."
        
        # Speak the response
       
        return response
