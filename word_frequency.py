import string
import asyncio
from collections import defaultdict, Counter
import httpx
import matplotlib.pyplot as plt

async def get_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

async def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

async def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

async def map_reduce(text):
    text = await get_text(url)
    if text:
        text = text.translate(str.maketrans("", "", string.punctuation))
        words = text.split()
        mapped_values = await asyncio.gather(*[map_function(word) for word in words])
        shuffled_values = shuffle_function(mapped_values)
        reduced_values = await asyncio.gather(*[reduce_function(key_values) for key_values in shuffled_values])

        return dict(reduced_values)
    else:
        return None
    
def visualize_top_words(result):
    top_10 = Counter(result).most_common(10)
    labels, values = zip(*top_10)
    plt.figure(figsize=(10, 6))

    # getting a color map with the spectrum from blue to yellow
    color_map = plt.colormaps.get_cmap('plasma')

    # number of columns
    num_bars = len(labels)

    # create a gradient
    colors = [color_map(i / num_bars) for i in range(num_bars)]

    bars = plt.barh(labels[::-1], values[::-1], color=colors[::-1])
    
    # change the direction of the x-axis labels 
    # so that they are rotated 45 degrees counter-clockwise
    plt.xticks(rotation=-45)

    # adding text next to the columns of a horizontal bar chart
    for bar, value in zip(bars, values[::-1]):
        plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f'{value}', ha='left', va='center')
    
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 most frequent words')
    plt.show()

if __name__ == '__main__':

    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    result = asyncio.run(map_reduce(url))
    # print("Word count result:", result)

    visualize_top_words(result)