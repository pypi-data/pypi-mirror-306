import sys
import argparse
import sqlite3

def check_and_insert_batch(batch, cursor, conn):
    cursor.execute('CREATE TEMPORARY TABLE IF NOT EXISTS temp_batch (value TEXT PRIMARY KEY)')
    cursor.execute('DELETE FROM temp_batch')
    cursor.executemany('INSERT INTO temp_batch (value) VALUES (?)', [(item,) for item in set(batch)])

    cursor.execute('SELECT seen.value FROM seen JOIN temp_batch ON seen.value = temp_batch.value LIMIT 1')
    if cursor.fetchone():
        sys.exit(1)  # Exit with status 1 if a duplicate is found

    cursor.execute('INSERT INTO seen SELECT temp_batch.value FROM temp_batch')
    conn.commit()

def configure_database(cursor, pragmas):
    # Apply each pragma provided by the user
    for pragma in pragmas:
        cursor.execute(f"PRAGMA {pragma}")

def main():
    parser = argparse.ArgumentParser(description="Check if a series of lines is partitioned (all identical lines sequential).")
    parser.add_argument('--chunk-size', type=int, default=1000000, help="Number of lines to process in each chunk (default: 1,000,000)")
    parser.add_argument('--pragmas', type=str, nargs='*', default=[], 
                        help="SQLite PRAGMA statements to configure the database (e.g., cache_size=-2000, threads=4)")
    parser.add_argument('input_file', type=str, nargs='?', help="Path to the input file (optional). If not provided, reads from stdin.")
    
    args = parser.parse_args()

    # Connect to a temporary SQLite database on disk (empty filename)
    conn = sqlite3.connect('')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS seen (value TEXT PRIMARY KEY)')
    conn.commit()

    # Configure database with user-specified pragmas
    configure_database(cursor, args.pragmas)

    current_chunk = []
    prev = None

    input_stream = sys.stdin if args.input_file is None else open(args.input_file, 'r')
    tried_chunk = False
    try:
        for line in input_stream:
            if prev is None or prev != line:
                current_chunk.append(line)
                prev = line

            if len(current_chunk) >= args.chunk_size:
                check_and_insert_batch(current_chunk, cursor, conn)
                current_chunk = []

        if current_chunk:
            check_and_insert_batch(current_chunk, cursor, conn)
        if not tried_chunk and len(set(current_chunk)) != len(current_chunk):
            sys.exit(1)
        tried_chunk = True

    finally:
        if args.input_file:
            input_stream.close()
        conn.close()

if __name__ == "__main__":
    main()

