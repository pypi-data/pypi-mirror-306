import sqlite3
import sys
import argparse

def check_and_insert_batch(batch, cursor, conn):
    # Create a temporary table and insert the batch
    cursor.execute('CREATE TEMPORARY TABLE IF NOT EXISTS temp_batch (value TEXT PRIMARY KEY)')
    cursor.execute('DELETE FROM temp_batch')  # Clear any previous data
    cursor.executemany('INSERT INTO temp_batch (value) VALUES (?)', [(item,) for item in set(batch)])

    # Check for duplicates with explicit table prefixes to avoid ambiguity
    cursor.execute('SELECT seen.value FROM seen JOIN temp_batch ON seen.value = temp_batch.value LIMIT 1')
    if cursor.fetchone():
        sys.exit(1)  # Exit with status 1 if a duplicate is found

    # Insert new items from the temporary table to the main table
    cursor.execute('INSERT INTO seen SELECT temp_batch.value FROM temp_batch')
    conn.commit()

def main(input_stream, chunk_size):
    # Connect to an SQLite database (in memory)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS seen (value TEXT PRIMARY KEY)')
    conn.commit()

    current_chunk = []
    prev = None
    for line in input_stream:
        if prev is None or prev != line:
            current_chunk.append(line)
            prev = line

        # When the chunk is full, process it
        if len(current_chunk) >= chunk_size:
            check_and_insert_batch(current_chunk, cursor, conn)
            current_chunk = []

    # Process any remaining lines in the last partial chunk
    if current_chunk:
        check_and_insert_batch(current_chunk, cursor, conn)

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if a sequence of strings streamed from stdin or a file is partitioned (all identical lines grouped sequentially). Exits 1 if not.")
    parser.add_argument('input_file', type=str, nargs='?', help="Path to the input file (optional). If not provided, reads from stdin.")
    parser.add_argument('--chunk-size', type=int, default=1000000, help="Number of lines to process in each chunk (default: 1,000,000)")

    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, 'r') as f:
            main(f, args.chunk_size)
    else:
        main(sys.stdin, args.chunk_size)
