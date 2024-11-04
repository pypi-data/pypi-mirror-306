
## Installation

```pip
pip install kvrocks-dao
```


setup config.ini in the root of project

```ini
    [kvrocks]
    host = 0.0.0.0
    port = 6666
```

## Examples

```py
    from kvrocks_dao import BaseDAO, BaseEntity

    class MediaEnity(BaseEntity):
        def __init__(self, _id: int, name: str, type: int):
            super().__init__(_id)
            self.name = name
            self.type = type

    class MediaDao(BaseDAO[MediaEnity]):
        def __init__(self):
            super().__init__(MediaEnity, "media")

    dao = MediaDao()

   # --- or ---

    dao = BaseDAO.from_entity(MediaEnity, "media")

    # get 
    # return MediaEnity
    media = dao.get(_id)

    # set
    media = Media(1, "Nhớ", 10)
    dao.set(media)


    # set from dataframe
    for _, row in df.iterrows():
        media = MediaEnity.from_dict(row.to_dict())
        print(media.to_dict())
        dao.set(media)

    # count
    dao.count()   

    # get list 
    # return List[tuple[int, MediaEnity]]
    dao.mget()

```

