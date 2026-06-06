import urllib.parse
import base64

def encode_file_lines(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            # URL encode with ',' and '.' excluded
            url_encoded = urllib.parse.quote(line, safe='-,.')
            # Convert to Base64 (text to bytes, then encode)
            base64_encoded = base64.b64encode(url_encoded.encode('utf-8')).decode('utf-8')
            outfile.write(base64_encoded + '\n')

# Példa hívás
encode_file_lines('kat1_2025_07_21.txt', 'kodolt_kategoriak_2025_07_21.txt')