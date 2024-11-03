def get_tables():
  return safe_read_from(os.path.dirname(os.path.abspath(__name__)),'solana_db_tables.json')
