def load_template(file_path):
    """Loads an HTML template file"""
    with open(file_path, "r") as template:
        return template.read()
    
def serialize_movies(movies_obj):
    """Serializes an movies object into HTML format"""
    output = ""
    output += f'<li>\n'
    output += f'  <div class="movie">'
    output += f'    <img class="movie-poster" src=f"{movies_obj["poster"]}">\n'
    output += f'    <div class="movie-title">{movies_obj["title"]}</div>\n'
    output += f'    <div class="movie-year">{movies_obj["year"]}</div>\n'
    output += f'  </div>\n'
    output += f'</li>\n'
    return output

def write_output(file_path, content):
    """Writes content to an output file"""
    with open(file_path, "w") as output_file:
        output_file.write(content)