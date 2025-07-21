def generate_script(products):
    script = "Welcome to our channel! Today, we’re comparing the top 3 Amazon picks. Let's dive in:\n\n"

    for i, p in enumerate(products, 1):
        title = p.get("title", "Product")
        price = p.get("price", "Price not available")
        link = p.get("link", "")
        # You can add pros and cons in your product dictionary if available
        pros = p.get("pros", "Great value and performance.")
        cons = p.get("cons", "Limited color options.")

        script += (
            f"{i}. {title}\n"
            f"Price: {price}\n"
            f"Use: This product is ideal for your daily needs and offers excellent performance.\n"
            f"Pros: {pros}\n"
            f"Cons: {cons}\n"
            f"Check it out here: {link}\n\n"
        )

    script += "Thanks for watching! Don’t forget to like, comment, and subscribe for more reviews.\n"
    return script
