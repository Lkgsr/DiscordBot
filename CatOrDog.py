import discord
from discord.ext import commands
import cv2
import tensorflow as tf
import numpy as np
import requests
CATEGORIES = ["Dog", "Cat"]


async def prepare(response):
    IMG_SIZE = 100  # 50 in txt-based
    image = np.asarray(bytearray(response.content), dtype="uint8")
    img_array = cv2.imdecode(image, cv2.cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


model = tf.keras.models.load_model("C:/Users/Lukas/PycharmProjects/"
                                   "DiscordBot/3-conv-64-nodes-0-dense-1540176132.model")


class CatOrDog:
    def __init__(self, client):
        self.client = client

    async def on_message(self, pic):
        if pic.attachments:
            for attachment in pic.attachments:
                print(attachment['url'])
                r = requests.get(attachment['url'], allow_redirects=True)
                x = await prepare(r)
                prediction = model.predict([x])
                print(prediction[0])
                obj = 'Nicht Vorhanden'
                num1, num2 = prediction[0]
                if num1 < 1 and num2 < 1:
                    obj = ' Hund'
                if num1 < 1 and num2 >= 1:
                    obj = 'e Katze'
                if num1 >=1 and num2 >=1:
                    obj = ' HaydeKlum'
                if num1 >=1 and num2 < 1:
                    obj = ' Julian'
                await self.client.send_message(pic.channel, f"Das ist ein{obj}")
                await self.client.send_message(pic.channel, f"Debug Log prediction werte {prediction[0]}")


def setup(client):
    client.add_cog(CatOrDog(client))
