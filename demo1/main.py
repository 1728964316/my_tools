import httpx
from lxml import etree

base_url = "https://www.zhonghuadiancang.com/waiguomingzhu/9768/"


def interview(pg, index):
    # Get the response from the URL
    response = httpx.get(
        "https://www.zhonghuadiancang.com/waiguomingzhu/9768/" + pg + ".html"
    )
    # Parse the HTML and extract the content
    root = etree.HTML(response.text)
    content = root.xpath("/html/body/div[2]/div[2]/div/div/div[2]/h1/text()")
    # Iterate through the content
    for i in content:
        # Print the content and complete the file
        print(i, "完成")
        with open("text" + index + ".txt", "a", encoding="utf-8") as f:
            f.write(i + "\n")

    # Extract the content from the HTML
    content = root.xpath('//*[@id="content"]/p/text()')
    t = ""
    # Iterate through the content
    for i in content:
        # Append the content to the text file
        t += "  " + i + "\n"
    # Write the content to the text file
    with open("text" + index + ".txt", "a", encoding="utf-8") as f:
        f.write(t + "\t")


def start():
    # Initialize the index
    index = 0
    # Iterate through the pages
    for i in range(199584, 199628):
        # Call the interview function
        interview(str(i), str(int(index / 5)))
        # Increment the index
        index += 1


if __name__ == "__main__":
    # Start the program
    start()
