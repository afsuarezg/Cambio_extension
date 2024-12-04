import os
import pypandoc
import win32com.client as win32


def pypandoc_convert_rtf_to_txt(input_file, output_file):
    output = pypandoc.convert_file(input_file, 'plain', format='rtf')
    with open(output_file, 'w') as txt_file:
        txt_file.write(output)


def get_substring_up_to_first_dot(s):
    """
    Returns the substring up to the first dot in the given string from left to right.

    Args:
        s (str): The input string.

    Returns:
        str: The substring up to the first dot, or the entire string if no dot is found.
    """
    dot_index = s.find('.')
    if dot_index != -1:
        return s[:dot_index]
    else:
        return s
    

def win32_convert_rtf_to_txt(input_file, output_file):
    # Create an instance of the Word application
    word = win32.Dispatch('Word.Application')
    word.Visible = False  # Run Word in the background

    try:
        # Open the input RTF document
        doc = word.Documents.Open(input_file)
        
        # Save as plain text file
        doc.SaveAs(output_file, FileFormat=2)  # 2 is the format code for plain text
        doc.Close(False)  # Ensure no save prompts

        return None

    except Exception as e:
        print(f"Error converting file: {e}")
        return input_file
    
    finally:
        # Close the document and quit Word application
        word.Quit()


def save_list_to_txt(lst, output_file):
    with open(output_file, 'w') as txt_file:
        for item in lst:
            txt_file.write(str(item) + '\n')


def get_files_in_folder(folder_path):

    return [os.path.join(folder_path, file) for file in os.listdir(folder_path)]


def get_filename_without_extension(file_path):
    # Extracts the filename without the extension
    return os.path.splitext(os.path.basename(file_path))[0]


def main(path_to_rtf_files, results_folder, files_with_error_folder):

    files = get_files_in_folder(path_to_rtf_files)
    files_not_processed = []
    for file in files: 
        try:
            filename = get_filename_without_extension(file)
            print(filename)
            transform_file = win32_convert_rtf_to_txt(file, rf'{results_folder}\{filename}.txt')   
            if transform_file != None:
                files_not_processed.append(file)
        except:
            files_not_processed.append(file)

    save_list_to_txt(files_not_processed, fr'{files_with_error_folder}\files_not_processed.txt')


if __name__=='__main__':
    main(r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\USB_Corte\2022', 
         r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\processed_files\2022',
         r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\processed_files\files_not_processed')
