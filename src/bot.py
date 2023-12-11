import os
from openai import OpenAI
# from config import OPENAI_KEY

client = OpenAI(
    api_key=os.environ.get('OPENAI_KEY')
)


def ask_gpt(current_map, current_side, current_round, results, money, total_kills, total_deaths):
    prompt = f"""
            Current Map: {current_map}
            Current Side: {current_side}
            Current Round: {current_round}
            Past Results: {results}
            Money: {money}
            Kills: {total_kills}
            Deaths: {total_deaths}

            Provide a strategy for what positions to take, what to buy, and how we should approach this round only. 
            In order to do this correctly, you must base your strategy off of what round we're in and the past results. 
            
            Predict if the other team has the money to full-buy, save, or eco. Also predict, what they may do based on 
            where the game is at to give me in order to give me as much of an advantage as possible.

            Key things to remember:
            - If its the first round, or the first round on a new side we wont have money to buy rifles.
            - There are only 5 players on each team.

            Provide the strategy in very-short summary/bullet-point format.
            Do not give generic advice or too much "fluff", just short and sweet.
            
            Buy:
            Positions:
            Approach:
            Prediction:
            """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a shot-caller for Counterstrike 2."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0
    )

    # Return the generated response
    return response.choices[0].message.content
