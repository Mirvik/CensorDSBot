import re
from langdetect import detect
from googletrans import Translator
import discord
from discord.ext import commands
# from discord.components import Component, ButtonComponentPayload, ButtonStyle
import detection
from allowedCategories import AllowedCategories


def blur_word(text, target_words):
 
    def childrenFn(text, target_word):
        original_language = detect(text)

        translator = Translator()
        translated_target_word = translator.translate(target_word, src="en", dest=original_language).text

        blurred_text = re.sub(rf'{translated_target_word}', lambda match: '#' * len(match.group()), text, flags=re.IGNORECASE)

        return blurred_text
 
    for target_word in target_words:
        text = childrenFn(text, target_word  )



    return text


def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest="en")
    return translated_text.text

def get_categories_str(hate_detections):
    str = ''

    for word in hate_detections[1]:
        str += f'\n {word[1]}'

    return str



# original_text = "твоя мать сука."
# target_word = "bitch"
 
# blurred_text = blur_word_in_different_language(original_text, target_word, "en"  )
# print(blurred_text)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

allowed_categories = AllowedCategories(set())



@bot.event
async def on_message(message):
    await bot.user.edit(username='CensorBotKamyk')

    if (message.author.name == bot.user.name):
        return


    hate_detections = detection.f(translate_text(message.content.lower()))
    if(message.content.startswith('!changenick')):
        bot.user.edit(username= 'CensurbotKamyk') 
    elif (message.author == bot.user):
        return
    
    elif (message.content.startswith('!add_category')):
        # await message.channel.send(
        #     components=[
        #         ButtonComponentPayload(style=ButtonStyle.green, label="Кнопка 1"),
        #         ButtonComponentPayload(style=ButtonStyle.red, label="Кнопка 2"),
        #         ButtonComponentPayload(style=ButtonStyle.blue, label="Кнопка 3")
        #     ]
        # )
        return

    elif (message.content.startswith('!remove_category')):
        
        await message.channel.send(f'Categories: ----------------')

    elif(hate_detections[0]!= 'No Hate and Offensive') :
        try:
            arr_bad_word = []

            censored_message = message.content
            toBlur = detection.f(translate_text(message.content))[1]
            print(toBlur)
 
            if (len(toBlur) != 0):
                for word_and_category in toBlur:
                    arr_bad_word.append(word_and_category[0])
            
            censored_message = blur_word(text=censored_message, target_words=arr_bad_word)
            


            print(censored_message)
            await message.delete()

            if (censored_message != message.content):
                await message.channel.send(f'{message.author.name}: {censored_message}')
            else:
                await message.channel.send(f'{message.author.name}: message was removed')

            await message.author.send(f'{censored_message}  Your message was removed, because you used {hate_detections[0]}:\n {get_categories_str(hate_detections)}')

        except:
            return



    
bot.run('MTIxODI4MzY0ODA1NTM3ODA4MQ.G6BaYm.r9GaIDRpSxe5vrawhJk6_-W-1Q-LkprvpiivYQ')