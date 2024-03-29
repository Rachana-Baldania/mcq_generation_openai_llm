from langchain.document_loaders import YoutubeLoader

from app.schemas.langchain_schemas.url_schema import UrlSchema


async def parse_youtube_video(url: UrlSchema):
    """
    Given a youtube url loads it's transcript into documents.

    Args:
        url (str): A valid url of youtube video.

    Returns:
        List[Document]: Each document represents a peice of youtube video transcript.

    https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/youtube_transcript

    """

    loader_params = {"url": url.url, "add_video_info": True}
    url.create_documents(
        Loader_class=YoutubeLoader.from_youtube_url, loader_params=loader_params
    )
    return
