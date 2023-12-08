# from openai import OpenAI
# from config import OPENAI_KEY
#
# client = OpenAI(
#     api_key=OPENAI_KEY
# )
#
# prompt = f"""
#         Current Map: {selected_map}
#         Current Round: {r}
#         Current Side: {starting_side}
#         Past Results: {results}
#
#         Provide a strategy detailing what positions to take, what to buy, and how we should approach the current round. In order to do this correctly, you
#         must base your strategy off of what round we're in and the past results. You must deduce how much money we have based on
#         the current round, and the past results.
#
#         For example, if its the first round we wont have money to buy rifles. Also, if it is the first round on a new side, we wont
#         have money for rifles either.
#
#         Also, predict if the other team has the money to buy, save, eco, or what they may do based on where the game is at to give me
#         as much of an advantage as possible with your help.
#
#         Provide the strategy in short summary/bullet-point format so that I can read it off to my team each round.
#         Do not give generic advice.
#         """
#
#
# def ask_gpt(prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a shot-caller for Counterstrike 2."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=2000,
#         temperature=0
#     )
#
#     # Return the generated response
#     return response.choices[0].message.content
