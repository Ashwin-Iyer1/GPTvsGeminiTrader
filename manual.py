from script import buy_multiple_eql_amts
import Gemini
import chatGPT


def Gemini():
    i = 0
    while i < 10:
        try:
            Gemini_content = Gemini.main()
            print(Gemini_content)
            numstocks = len(Gemini_content)
            buys = buy_multiple_eql_amts(Gemini_content, 3000/numstocks, 'gemini')
            if buys:
                break
        except Exception as e:
            print(f"Gemini Error occurred: {e}")
        i += 1
def GPT():
    i = 0
    while i < 10:
        try:
            OpenAI_content = chatGPT.main()
            print(OpenAI_content)
            numstocks = len(OpenAI_content)
            buys = buy_multiple_eql_amts(OpenAI_content, 3000/numstocks, 'openai')
            if buys:
                break
        except Exception as e:
            print(f"OpenAI Error occurred: {e}")
        i += 1

chosenplatform = input("Enter the platform you want to use: ")
if chosenplatform == 'gemini':
    Gemini()
elif chosenplatform == 'openai':
    GPT()
