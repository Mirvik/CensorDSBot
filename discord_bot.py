import re
from typing import Any
from langdetect import detect
from googletrans import Translator
import discord
from discord.ext import commands
import detection
from allowedCategories import AllowedCategories
from skam import check

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

allowed_categories = AllowedCategories(set())

class ChooseFilterCategories(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=category, value=category) for category in AllowedCategories.badWordsCategories
        ]

        super().__init__(options=options, placeholder="Choose categories to blur words",max_values=len(AllowedCategories.badWordsCategories) - 1)

    async def callback(self, interaction):
        await self.view.choosenCategoriesRespond(interaction, self.values)

class FilterCategoryView(discord.ui.View):
    answer = None
    choosenCategories = None

    @discord.ui.select(
        placeholder="With what categories words should be blured",
        options=[
            discord.SelectOption(label='Every category', value='every'),
            discord.SelectOption(label='Choose some categories', value='choose'),
        ]
    )
    async def select_age(self, interaction: discord.Integration, select_item: discord.ui.Select):
        self.answer = select_item.values
        self.children[0].disabled = True
        if self.answer[0] != 'every':
            categoriesSelect = ChooseFilterCategories()
            self.add_item(categoriesSelect)

        await interaction.message.edit(view=self)
        await interaction.response.defer()
        if self.answer[0] == 'every':
            self.stop()

    async def choosenCategoriesRespond(self, interaction: discord.Integration, choices):
        self.choosenCategories = choices
        await interaction.response.defer()
        self.stop()



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
        str += f'\n **{word[1]}**'

    return str





# original_text = "твоя мать сука."
# target_word = "bitch"
 
# blurred_text = blur_word_in_different_language(original_text, target_word, "en"  )
# print(blurred_text)



@bot.event
async def on_message(message):
    await bot.user.edit(username='CensorBotKamyk')

    if (message.author.name == bot.user.name):
        return


    hate_detections = detection.f(translate_text(message.content.lower()))
    # if(message.content.startswith('!select_menu')):
    #     allowed_categories.clear()
    #     view = FilterCategoryView()
    #     await message.channel.send(view=view)

    #     await view.wait()
    #     if view.answer[0] == 'choose':
    #         for c in view.choosenCategories:
    #             allowed_categories.pushCategory(c)

    if (message.author == bot.user):
        return

    elif (message.author.guild_permissions.administrator and message.content.startswith('!set_categories')):
        
        allowed_categories.clear()
        view = FilterCategoryView()
        await message.channel.send(view=view)

        await view.wait()
        if view.answer[0] == 'choose':
            for c in view.choosenCategories:
                allowed_categories.pushCategory(c)

        print(allowed_categories.getAllowedCategories())

    elif (check(translate_text(message.content)) == True):

        await message.delete()
        await message.channel.send('Warning! It\'s a scam')

    elif(hate_detections[0]!= 'No Hate and Offensive') :
        try:
            arr_bad_word = []

            censored_message = message.content
        
            toBlur = allowed_categories.filterWords(hate_detections[1]) 
            print(toBlur)
 
            if (len(toBlur) != 0):
                for word_and_category in toBlur:
                    arr_bad_word.append(word_and_category[0])
            
            censored_message = blur_word(text=censored_message, target_words=arr_bad_word)
            


            print(censored_message)
            await message.delete()

            if (censored_message != message.content):
                await message.channel.send(f'***{message.author.name}*** : {censored_message}')
            else:
                await message.channel.send(f'***{message.author.name}*** : **message was removed**')

            await message.author.send(f'***{message.author.name}***  Your message was removed, because you used {hate_detections[0]}:\n {get_categories_str(hate_detections)}')

        except:
            return



@bot.command()
async def select_menu(ctx):
    allowed_categories.clear()
    view = FilterCategoryView()
    await ctx.send(view=view)

    await view.wait()
    if view.answer[0] == 'choose':
        for c in view.choosenCategories:
            allowed_categories.pushCategory(c)

    print(allowed_categories.getAllowedCategories())


    
bot.run('MTIxODI4MzY0ODA1NTM3ODA4MQ.GOk1sZ.ZArVqsUIPOPm9luwz2nWxUHzVaRaBCNjiAcJwU')