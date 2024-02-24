# import os
# from openai import OpenAI
# from config import OPENAI_KEY

# client = OpenAI(
#     api_key=os.environ.get('OPENAI_KEY')
#     # api_key=OPENAI_KEY
# )


# def ask_gpt(current_map, current_side, current_round, results, money, total_kills, total_deaths):
#     prompt = f"""
#             Use the provided game data, your creativity, and the following steps to deliver Counter-Strike 2 strategies
#             in order to give my team as much of an advantage as possible:
#
#              - The strategy is for the Current Round and Current Map only.
#              - Provide what positions to take according to the Current Side and Current Map.
#              - Provide what to buy based on how much Money I have and the Past Results.
#              - Provide the approach to be taken based on the positions you provided/
#              - Predict if the other team has the money to full-buy, full-save, or eco based on the Past Results.
#              - Predict how the other team may play the Current Round based on the Past Results.
#              - Deliver the response succinctly with minimal explanation.
#
#             ## Game Data
#
#             Current Map: {current_map}
#             Current Side: {current_side}
#             Current Round: {current_round}
#             Past Results: {results}
#             Money: {money}
#             My Kills: {total_kills}
#             My Deaths: {total_deaths}
#
#             ## Final Notes:
#
#             - On the 1st and 13th rounds, teams switch sides, and the economy resets for both teams.
#             - There are only 5 players on a team.
#             """
#
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a Counter-Strike 2 shot caller."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=2000,
#         temperature=0
#     )
#
#     # Return the generated response
#     return response.choices[0].message.content
