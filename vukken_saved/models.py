from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DownloadableResourceMixin():
    is_downloaded = Column(Boolean)


class RawFieldMixin():
    raw = Column(String, nullable=False)


class RecordOwnerMixin():
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, primary_key=True)


class Photo(Base, RecordOwnerMixin, RawFieldMixin):
    __tablename__ = "photo"
    resized = relationship("PhotoResized", back_populates="photo")

    def __init__(self, *args, **kwargs):
        kwargs["id"] = kwargs["raw"]["id"]
        kwargs["owner_id"] = kwargs["raw"]["owner_id"]
        super(Photo, self).__init__(*args, **kwargs)


class PhotoResized(Base, DownloadableResourceMixin):
    __tablename__ = "photo_resized"
    photo_id = Column(Integer, ForeignKey("photo.id"), primary_key=True)
    size_type = Column(String, index=True)
    width = Column(Integer)
    heigth = Column(Integer)
    photo = relationship("Photo", back_populates="resized")


class Post(Base, RecordOwnerMixin, RawFieldMixin):
    __tablename__ = "post"

    def __init__(self, *args, **kwargs):
        if "raw" not in kwargs and len(args) > 0:
            kwargs["raw"] = args[0]
            args = args[1:]

        if "id" not in kwargs:
            kwargs["id"] = kwargs["raw"]["id"]

        if "owner_id" not in kwargs:
            kwargs["owner_id"] = kwargs["raw"]["owner_id"]

        return super(Post, self).__init__(*args, **kwargs)

    def extract_copy_history(self):
        for x in self.raw.get("copy_history", []):
            yield Post(id=x["id"], owner_id=x["owner_id"], raw=x)

    def extract_photo(self):
        photo_attachments = filter(
            lambda x: x["type"] == "photo",
            self.raw.get("attachments", [])
        )
        for x in photo_attachments:
            yield Photo(raw=x)
