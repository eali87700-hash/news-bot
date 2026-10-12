import feedparser
from supabase import create_client, Client
import os

SUPABASE_URL = "https://bbqkiwnpcmhtxvrprzeb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJicWtpd25wY21odHh2cnByemViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk0MjAwMDAsImV4cCI6MjA0NDk5NjAwMH0.placeholder"

RSS_SOURCES = [
    {"url": "https://www.aljazeera.net/rss", "category": "سياسية وعامة", "source": "الجزيرة"},
    {"url": "https://www.reuters.com/arc/outboundfeeds/v1/category/business/?outputType=xml", "category": "اقتصادية", "source": "رويترز"},
    {"url": "https://www.kooora.com/default.aspx?r=rss", "category": "رياضية", "source": "كوورة"},
    {"url": "https://www.skynewsarabia.com/rss", "category": "منوعة وثقافية", "source": "سكاي نيوز عربية"},
    {"url": "https://www.theverge.com/rss/index.xml", "category": "تكنولوجيا", "source": "The Verge"}
]

def fetch_all_fields_news():
    url = os.environ.get("SUPABASE_URL", SUPABASE_URL)
    key = os.environ.get("SUPABASE_KEY", SUPABASE_KEY)
    supabase: Client = create_client(url, key)
    
    for source_info in RSS_SOURCES:
        feed_url = source_info["url"]
        default_category = source_info["category"]
        source_name = source_info["source"]
        
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "بدون عنوان")
                summary = entry.get("summary", title)
                source_url = entry.get("link", "#")
                
                if "<" in summary:
                    summary = title
                
                existing = supabase.table("news").select("id").eq("source_url", source_url).execute()
                
                if not existing.data:
                    data = {
                        "title": title,
                        "summary": summary[:250],
                        "category": default_category,
                        "source_name": source_name,
                        "source_url": source_url
                    }
                    supabase.table("news").insert(data).execute()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    fetch_all_fields_news()
