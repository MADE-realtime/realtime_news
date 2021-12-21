cd ../
/code/parser/.venv/bin/python parse_news.py -d vk.json vk_db -start_urls source_files/vk.url
/code/parser/.venv/bin/python parse_news.py -d rss_news.json rss_db -s source_files/smi.url -r data_collection/rss_parser.yaml
/code/parser/.venv/bin/python parse_tg.py get_last -to_db