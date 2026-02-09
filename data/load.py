def save_item(container, id, content, vector, metadata):
    item = {
        "id": id,
        "content": content,
        "contentVector": vector
    }
    item.update(metadata)

    container.upsert_item(item)
    print(f"saved item={id} successfully")