from kivy.app import App
from kivy.config import Config
import os
from kivy.lang import Builder
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'top', 0)
Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
# Set the background color
from kivy.core.window import Window
#Window.clearcolor = (.02,.02,.02)  # RGB color with full opacity (A = 1)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty,ListProperty, StringProperty,NumericProperty
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
from kivy.clock import Clock
from pygments.lexers import guess_lexer, TextLexer, DiffLexer
from pygments.styles import get_style_by_name
from sigit.custom_widgets import CustomPopup
from sigit.custom_widgets import CustomDropdown
from sigit.custom_widgets import CustomDropBtn
import datetime
import re
import subprocess
import argparse


# Get the directory where the current file is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the font file in the assets directory
font_path = os.path.join(current_dir, 'assets', 'fonts', 'DejaVuSansMono.ttf')

# Register the font with Kivy
LabelBase.register(
    name="DejaVuSansMono",
    fn_regular=font_path,  # Use the dynamically generated path
)

# Predefined list of branch colors (normalized RGB)
BRANCH_COLORS = [
    '#FF5733',  # Red-Orange
    '#33FF57',  # Green
    '#3357FF',  # Blue
    '#FF33A1',  # Pink
    '#33FFF5',  # Cyan
    '#F5FF33'   # Yellow
]

class MainWidget(BoxLayout):
    selection = StringProperty('')
    repo_name = StringProperty('')
    parsed_arguments = StringProperty('')
    marked_commit = StringProperty('')
    is_patch_view = BooleanProperty(True)
    commits = {}
    command_history = []  # Store all the git log command arguments
    current_index = NumericProperty(-1)  # Track the current position; -1 means no logs yet
    def __init__(self,parsed_arguments, **kwargs):
        self.parsed_arguments = ' '.join(parsed_arguments) if parsed_arguments else ''
        print(self.parsed_arguments)
        super(MainWidget, self).__init__(**kwargs)    
        self.get_git_log(parsed_arguments=parsed_arguments)
        try:
            repo_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], universal_newlines=True).strip()
            self.repo_name = repo_path.split('/')[-1]  # Extract the repository name from the full path
        except subprocess.CalledProcessError as e:
            self.repo_name="Error: Not a valid Git repository"

    def get_branch_color(self, branch_index):
        """Get the hex color for a branch based on its index."""
        return BRANCH_COLORS[branch_index % len(BRANCH_COLORS)]  # Rotate through hex colors
    
    def colorize_graph_part(self, graph_part):
        """
        Takes the ASCII graph part and applies colors to different symbols based on branch position.
        This preserves merge and diverge symbols (|, \, /, *) while coloring them.
        """
        colored_graph = ""
        branch_positions = [i for i, char in enumerate(graph_part) if char in "|*\\/" ]  # Symbols representing branches

        for i, char in enumerate(graph_part):
            if char in "|*\\/":  # If the char is part of the graph branch structure
                branch_index = branch_positions.index(i) if i in branch_positions else 0
                color = self.get_branch_color(branch_index)  # Get corresponding branch color
                colored_graph += f"[color={color}]{char}[/color]"
            else:
                colored_graph += char  # Non-branch symbols (e.g., spaces, commit hashes)
        return colored_graph
    
    def go_back(self):
        # Move back in the command history
        if self.current_index > 0:
            self.current_index -= 1
            self.get_git_log(self.command_history[self.current_index], add_to_history=False)

    def go_forward(self):
        # Move forward in the command history
        if self.current_index < len(self.command_history) - 1:
            self.current_index += 1
            self.get_git_log(self.command_history[self.current_index], add_to_history=False)
    
    def on_current_index(self, *args):
        # Enable or disable back button
        if self.current_index <= 0:
            self.prev_btn.disabled = True
        else:
            self.prev_btn.disabled = False

        # Enable or disable forward button
        if self.current_index >= len(self.command_history) - 1:
            self.next_btn.disabled = True
        else:
            self.next_btn.disabled = False

        # Extract the command from the command history
        current_command = self.command_history[self.current_index]

        # Remove the base git command from the current command
        base_command = ('git', 'log', '--graph', '--pretty=format:%H - %s - %an - %ad', '--date=local')
        arguments_only = current_command[len(base_command):]

        # Save the remaining arguments as a string to self.parsed_arguments
        self.parsed_arguments = ' '.join(arguments_only) if arguments_only else ''

    def get_git_log(self, git_command=('git', 'log', '--graph', '--pretty=format:%H - %s - %an - %ad', '--date=local'), parsed_arguments=None, add_to_history=True):
        if parsed_arguments:
            # Convert list to tuple and combine
            git_command = git_command + tuple(parsed_arguments)
        try:
            # Run the command
            git_log_output = subprocess.check_output(git_command, universal_newlines=True)
            commit_lines = git_log_output.splitlines()

            # Call the new method to handle displaying the log
            self.display_log_output(commit_lines)

            # Add the command to history only if it succeeds and if `add_to_history` is True
            if add_to_history:
                self.command_history.append(git_command)
                self.current_index = len(self.command_history) - 1  # Set the current index to the latest command

        except subprocess.CalledProcessError as e:
            self.commit_list.add_widget(Label(text="Error running git log", size_hint_y=None, height=40))

    def display_log_output(self, commit_lines):
        self.all_commits = {}
        last_commit_date = None  # To track the date of the last commit

        for i, commit in enumerate(commit_lines):
            # Split into graph part and commit details
            parts = commit.split(' - ', 1)
            if len(parts) > 1:
                graph_part = parts[0]  # This includes the graph (with merge/diverge lines) and commit hash
                commit_details = parts[1]  # The rest after the first split

                # Split the commit details into components (message, author, date)
                details_parts = commit_details.split(' - ')
                if len(details_parts) == 3:
                    message, author, date = details_parts
                    commit_hash = graph_part.strip().split()[-1]  # Get the commit hash
                    graph_part = graph_part[:graph_part.rfind(commit_hash)].rstrip()  # Extract just the graph part

                    # Check if the commit is a subrepo commit
                    is_subrepo_commit, subrepo_commit_hash = self.check_subrepo_in_commit(commit_hash)

                    # Prefix message if it's a subrepo commit
                    if is_subrepo_commit:
                        message = f"[SUBREPO] {message}"
                        self.get_subrepo_history(subrepo_commit_hash)

                    # Colorize the graph part (break into segments and apply colors)
                    colored_graph_part = self.colorize_graph_part(graph_part)
                    last_commit_date = date

                    # Add the commit line to the data
                    self.all_commits[commit_hash] = {
                        'graph': colored_graph_part,
                        'commit_hash': commit_hash,
                        'message': message,
                        'author': author,
                        'date': date
                    }

            else:
                # Handle pure graph lines (like "|/" or "|")
                graph_part = commit.strip()
                if "|" in graph_part:
                    # Detect branch divergence/convergence
                    colored_graph_part = self.colorize_graph_part(graph_part)
                    # Add a line with only the graph part, leaving the rest empty
                    self.all_commits[f'graph_{i}'] = {
                        'graph': colored_graph_part,
                        'commit_hash': '',
                        'message': '',
                        'author': '',
                        'date': last_commit_date if last_commit_date else datetime.now()  # If for some reason latest commit line is ascii only
                    }

        # Set commit_list data and select the latest commit
        self.commit_list.data = [
            {
                'graph': commit['graph'],
                'commit_hash': commit['commit_hash'],
                'message': commit['message'],
                'author': commit['author'],
                'date': commit['date'],
                'highlighted': False,
                'marked': False,
                'graph_length': len(commit['graph'])  # Store graph part length
            }
            for commit in self.all_commits.values()
        ]

        # Select the latest commit
        Clock.schedule_once(lambda dt: self.commit_list.commits.select_item_by_index(0), 0)

    def check_subrepo_in_commit(self, commit_hash):
        """
        Recursively check for subrepos in the given commit and handle nested subrepos.
        """
        try:
            # Fetch the full commit body using 'git show'
            commit_body = subprocess.check_output(
                ['git', 'show', '-s', '--pretty=format:%b', commit_hash],
                universal_newlines=True
            ).strip()

            # Regular expression to match 'git-subrepo:'
            subrepo_pattern = r'(?<!["\'])git-subrepo:(?!["\'])'
            
            # Regular expression to extract the subrepo commit hash from the commit body
            subrepo_commit_pattern = r'commit:\s*"(.+)"'

            # Check if 'git-subrepo:' is present in the commit body
            is_subrepo_commit = re.search(subrepo_pattern, commit_body) is not None

            # Extract the subrepo commit hash if present
            subrepo_commit_hash = None
            commit_match = re.search(subrepo_commit_pattern, commit_body)
            if commit_match:
                subrepo_commit_hash = commit_match.group(1)

            # Recursively check for nested subrepos
            #if is_subrepo_commit and subrepo_commit_hash:
                #print(f"Subrepo detected at commit {commit_hash}. Recursively checking...")
                #nested_subrepo_commits = []
                
                # Unpack all three return values from the recursive call
                #nested_is_subrepo, nested_subrepo_commit_hash, nested_subrepo_commits = self.check_subrepo_in_commit(subrepo_commit_hash)
                
                # If there's a nested subrepo, add it to the list
                # if nested_is_subrepo and nested_subrepo_commit_hash:
                #     print(f"Nested subrepo detected in {subrepo_commit_hash}.")
                #     nested_subrepo_commits.append(nested_subrepo_commit_hash)

                return is_subrepo_commit, subrepo_commit_hash# , nested_subrepo_commits

            return is_subrepo_commit, subrepo_commit_hash#, []

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving body for commit {commit_hash}: {e}")
            return False, None, []

    def get_subrepo_history(self, subrepo_commit_hash):
        try:
            # Fetch the subrepo commit history
            git_subrepo_log_output = subprocess.check_output(
                ['git', 'log', '--pretty=format:%h - %s - %an - %ad', '--date=local', subrepo_commit_hash],
                universal_newlines=True
            )

            subrepo_commit_lines = git_subrepo_log_output.splitlines()

            for commit in subrepo_commit_lines:
                # Split the commit into hash and details
                commit_hash, commit_details = commit.split(' - ', 1)

                details_parts = commit_details.split(' - ')
                if len(details_parts) == 3:
                    message, author, date = details_parts

                    # Get branches containing the commit
                    branches = subprocess.check_output(
                        ['git', 'branch', '--contains', commit_hash],
                        universal_newlines=True
                    ).strip().splitlines()

                    # Clean the branches list (remove asterisks and extra spaces)
                    cleaned_branches = [branch.replace('*', '').strip() for branch in branches]
                    
                    # Join the branches as the path (assuming the first branch can be the main subrepo path)
                    subrepo_path = ', '.join(cleaned_branches) if cleaned_branches else "Unknown branch"

                    # Insert the branches (subrepo path) into the graph field
                    self.all_commits[commit_hash] = {
                        'graph': f"Subrepo: {subrepo_path}",  # Path (branches) is now stored in the graph part
                        'commit_hash': commit_hash,
                        'message': f"[SUBREPO HISTORY] {message}",
                        'author': author,
                        'date': date,
                    }

        except subprocess.CalledProcessError as e:
            self.commit_list.add_widget(Label(text=f"Error retrieving subrepo history", size_hint_y=None, height=40))

    def perform_search(self, search_term, file_path=None, line_range=None):
        if not search_term:
            return

        search_option = self.ids.search_options.text
        parsed_arguments = []

        if search_option == 'Limit to Author':
            parsed_arguments.extend(['--author', search_term])
        elif search_option == 'Search Messages':
            parsed_arguments.extend(['--grep', search_term])
        elif search_option == 'Search Changes':
            parsed_arguments.extend(['-G', search_term])
        elif search_option == 'Search Occurrences':
            parsed_arguments.extend(['-S', search_term])
        elif search_option == 'Trace Line Evolution':
            if line_range and file_path:
                parsed_arguments.extend(['-L', f"{line_range}:{file_path}"])

        # Call get_git_log with the parsed arguments
        self.get_git_log(parsed_arguments=parsed_arguments)

    def get_tree(self, commit_hash):
        self.diff_scroll.text = '' # clear diff text
        try:
            # Get the tree data for the commit
            tree_output = subprocess.check_output(
                ['git', 'ls-tree', '-r', commit_hash],
                universal_newlines=True
            ).strip()

            # Parse the tree output and create a file-to-blob mapping
            file_structure, file_to_blob = self.parse_tree_output(tree_output)

            # Create a TreeView widget
            tree_view = TreeView(root_options=dict(text="Root"), hide_root=False)
            self.populate_tree_view(tree_view, file_structure)
            self.tree_box.clear_widgets()
            self.tree_box.add_widget(tree_view)

            # Save the file-to-blob mapping for quick blob lookup later
            self.file_to_blob = file_to_blob

            # Get commit details and update diff_box
            self.get_commit_details(commit_hash)

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving data for commit {commit_hash}: {e}")
            return None
        
    def parse_tree_output(self, tree_output):
        file_structure = {}
        file_to_blob = {}
        
        for line in tree_output.splitlines():
            parts = line.split(None, 4)
            if len(parts) == 4:
                mode, file_type, blob_hash, file_path = parts
                path_parts = file_path.split('/')
                current_level = file_structure

                for part in path_parts:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

                # Map the file path to the corresponding blob hash
                file_to_blob[file_path] = blob_hash
        
        return file_structure, file_to_blob

    def populate_tree_view(self, tree_view, file_structure, parent_node=None, base_path=""):
        for key, value in file_structure.items():
            # Construct the full path for the current file or directory
            current_path = f"{base_path}/{key}".lstrip('/')

            if value:  # If it's a directory
                # Add the directory as a TreeViewLabel and recursively populate its children
                node = tree_view.add_node(TreeViewLabel(text=key), parent_node)
                self.populate_tree_view(tree_view, value, node, current_path)
            else:  # If it's a file
                tree_label = TreeLabel(file=key, path=current_path, root_widget=self)
                node = tree_view.add_node(tree_label, parent_node)

                # Bind the file label to an event handler (e.g., to display its diff or open the file)
                # file_label.bind(on_touch_down=self.on_file_click)

    def on_file_click(self, file_path):
        # Get the file name and commit hash
        commit_hash = self.selection

        # Check if the file is a known binary format
        if file_path.endswith(('.ttf', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.exe', '.dll', '.zip', '.pdf')):
            print(f"{file_path} is a binary file. Cannot display.")
            self.diff_scroll.text = f"Cannot display binary file: {file_path}"
            return

        # Use 'git show' to get the content of the file at the specific commit
        try:
            # Fetch the content of the file as it was in the specified commit
            file_content = subprocess.check_output(
                ['git', 'show', f'{commit_hash}:{file_path}'],
                universal_newlines=True  # Fetch as text (handle binary separately if needed)
            ).strip()

            # Display the file content in diff_box
            self.display_file_content(file_content)

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving file content for {file_path} at commit {commit_hash}: {e}")
            self.diff_scroll.text = f"Error retrieving file content for {file_path} at commit {commit_hash}: {e}"
    
    def highlight_file_from_code(self, code_input):
        pass
    
    def display_file_content(self, file_content):
        # Set up the display logic for the file content
        self.diff_scroll.text = ""

        # Attempt to guess the correct lexer for the file content
        try:
            lexer = guess_lexer(file_content)
        except:
            # If guessing the lexer fails, fall back to plain text lexer
            lexer = TextLexer()

        # Apply the lexer and Zenburn style
        self.diff_scroll.lexer = lexer
        self.diff_scroll.style = get_style_by_name('zenburn')

        # Display the content
        self.diff_scroll.text = file_content

        # Move the cursor to the first line
        Clock.schedule_once(lambda dt: self.move_cursor_to_row(0))
    
    def get_commit_details(self, commit_hash):
        try:
            # Get parent commit hash
            parent_hash = subprocess.check_output(
                ['git', 'log', '--format=%P', '-n', '1', commit_hash],
                universal_newlines=True
            ).strip()

            # Get branches containing the commit
            branches = subprocess.check_output(
                ['git', 'branch', '--contains', commit_hash],
                universal_newlines=True
            ).strip().splitlines()

            # Remove the asterisk from the current branch and any leading/trailing whitespace
            cleaned_branches = [branch.replace('*', '').strip() for branch in branches]

            # Get full commit message
            commit_message = subprocess.check_output(
                ['git', 'show', '--format=%B', '-s', commit_hash],
                universal_newlines=True
            ).strip()

            # Get child commits by finding commits where the current commit is a parent
            child_commits = subprocess.check_output(
                ['git', 'rev-list', '--all', '--children'],
                universal_newlines=True
            ).strip().splitlines()

            # Filter out the child commits for the specific commit
            children = [
                line.split()[1:] for line in child_commits
                if line.startswith(commit_hash)
            ]
            # Flatten the list (in case there are multiple children)
            children = [commit for sublist in children for commit in sublist]

            # Generate links for parent, branches, and child commits
            parent_link = f'[ref={parent_hash}][color=00ccff][u]{parent_hash}[/u][/color][/ref]' if parent_hash else 'None'

            # Only display branch names without head commits
            branch_links = ', '.join([
                f'[ref={branch.strip()}][color=00ccff][u]{branch.strip()}[/u][/color][/ref]'
                for branch in cleaned_branches
            ])

            child_links = ', '.join([
                f'[ref={child}][color=00ccff][u]{child}[/u][/color][/ref]'
                for child in children
            ]) if children else 'None'
            
            self.commit_details.commit_hash_lbl.text = 'HASH: ' + commit_hash
            
            self.commit_details.parent_child_lbl.text = (
                f"Child Commits: {child_links}\n"
                f"Parent: {parent_link}"
            )
            self.commit_details.branch_lbl.text = f"Branches: {branch_links}"
            self.commit_details.message_lbl.text = '\n' + commit_message
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving commit details for {commit_hash}: {e}")
            return None
    
    def on_branch_click(self, instance, branch_name):
        try:
            # Get the head commit for the clicked branch
            head_commit = subprocess.check_output(
                ['git', 'rev-parse', branch_name],
                universal_newlines=True
            ).strip()
            for index, item in enumerate(self.commit_list.data):
                if item['commit_hash'] == head_commit:
                    self.commit_list.commits.select_item_by_index(index)

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving head commit for branch {branch_name}: {e}")
    
    def on_ref_press(self, instance, ref):
        for index, item in enumerate(self.commit_list.data):
            if item['commit_hash'] == ref:
                self.commit_list.commits.select_item_by_index(index)

    def get_files_changed(self, commit_hash):
        if not commit_hash:
            print("Invalid or empty commit hash. Skipping file change retrieval.")
            return None
        try:
            # Get the list of changed files directly using 'git show'
            changed_files_output = subprocess.check_output(
                ['git', 'show', '--name-only', '--pretty=format:', commit_hash],
                universal_newlines=True
            ).strip()

            # Clear the existing widgets in tree_box
            self.tree_box.clear_widgets()

            # Split the output to get the list of changed files (file paths)
            changed_files = changed_files_output.splitlines()

            # Iterate over each file path and add a FileLabel widget
            for file_path in changed_files:
                # Extract the file name from the file path
                file_name = file_path.split('/')[-1]  # This gets the last part of the path as the file name
                
                # Add the FileLabel with both file name and file path
                self.tree_box.add_widget(FileLabel(file=file_name, path=file_path, root_widget=self))

        except subprocess.CalledProcessError as e:
            print(f"Error retrieving data for commit {commit_hash}: {e}")
            return None

    def get_diff_output(self, commit_hash):
        if not commit_hash:
            print("Invalid or empty commit hash. Skipping file change retrieval.")
            return None
        try:
            # Get the diff for the commit
            diff_output = subprocess.check_output(
                ['git', 'diff', f'{commit_hash}^!', '--unified=3'],
                universal_newlines=True
            ).strip()

            return diff_output

        except subprocess.CalledProcessError as e:
            print(f"Error getting diff for commit {commit_hash}: {e}")
            return None

    def display_diff(self, commit_hash):
        # Get the commit details and display them first
        self.get_commit_details(commit_hash)

        # Get the diff output for the given commit hash
        diff_output = self.get_diff_output(commit_hash)

        # Clear the text content of diff_scroll (TextInput widget)
        self.diff_scroll.text = ""
        
        # Set the lexer and style for the diff view
        self.diff_scroll.lexer = DiffLexer()  # Apply your DiffLexer
        self.diff_scroll.style=get_style_by_name('zenburn')

        if not diff_output:
            # If no diff is available, display a message in the TextInput
            self.diff_scroll.text = "No diff data available\n"
            return

        # Directly assign the entire diff output to the TextInput, let lexer handle it
        self.diff_scroll.text = diff_output
        # Move to top of file 
        Clock.schedule_once(lambda dt: self.move_cursor_to_row(0))

    def on_selection(self, *args): 
        if self.selection is not None:
            if self.is_patch_view:
                self.display_diff(self.selection)
                self.get_files_changed(self.selection)
            else:
                self.get_tree(self.selection)

    def on_is_patch_view(self, *args):
        if self.selection is not None:
            if self.is_patch_view:
                self.display_diff(self.selection)
                self.get_files_changed(self.selection)
            else:
                self.get_tree(self.selection)
    
    def move_cursor_to_row(self, row):
        # Now set the cursor to the start of the line where the file begins
        self.diff_scroll.cursor = (0, row)
    
    def blame_parent_commit(self, file_path):
        if not self.selection:
            return
        try:
            # Run the git log command using subprocess
            result = subprocess.run(
                ['git', 'log', '--follow', '--format=%H', f'{self.selection}^', '--', file_path],  # Starting from parent
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Check if the command was successful
            if result.returncode != 0:
                print(f"Error running git log: {result.stderr}")
                return None

            # Split the output by lines and get the first commit
            commit_hashes = result.stdout.splitlines()
            if commit_hashes:
                for index, item in enumerate(self.commit_list.data):
                    if item['commit_hash'] == commit_hashes[0]:
                        self.commit_list.commits.select_item_by_index(index)
            else:
                # No commits found
                return None

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def highlight_commits_for_file(self, file_path, add_highlight=False):
        try:
            # Reset highlights if add_highlight is False
            if not add_highlight:
                for commit in self.commit_list.data:
                    commit['highlighted'] = False
            
            # Get all commit hashes where the file was changed
            changed_commits_output = subprocess.check_output(
                ['git', 'log', '--format=%H', '--', file_path],
                universal_newlines=True
            ).strip()

            # Convert the output to a set of commit hashes
            changed_commits = set(changed_commits_output.splitlines())

            # Highlight the relevant commits
            for commit in self.commit_list.data:
                if commit['commit_hash'] in changed_commits:
                    commit['highlighted'] = True  # Mark as highlighted

            self.commit_list.refresh_from_data()
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving commits for file {file_path}: {e}")
    
    def diff_commits(self, commit_a, commit_b):
        """Runs git diff between two commits."""
        try:
            result = subprocess.run(
                ['git', 'diff', commit_a, commit_b],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                # Set the lexer and style for the diff view
                self.diff_scroll.lexer = DiffLexer()  # Apply your DiffLexer
                self.diff_scroll.style=get_style_by_name('zenburn')    
                self.diff_scroll.text =  result.stdout  # display the diff output
                # Move to top of file 
                Clock.schedule_once(lambda dt: self.move_cursor_to_row(0))
            else:
                self.diff_scroll.text = f"Error: {result.stderr}"

        except Exception as e:
            return str(e)
    
    def mark_commit(self, commit_hash):
        # Check if the commit to be marked is already marked
        if self.marked_commit == commit_hash:
            # Unmark the current commit
            for commit in self.commit_list.data:
                if commit['commit_hash'] == self.marked_commit:
                    commit['marked'] = False
            self.marked_commit = ''  # No commit is marked now
        else:
            # Unmark the previous commit if it exists
            if self.marked_commit is not None:
                for commit in self.commit_list.data:
                    if commit['commit_hash'] == self.marked_commit:
                        commit['marked'] = False

            # Mark the new commit
            self.marked_commit = commit_hash
            for commit in self.commit_list.data:
                if commit['commit_hash'] == commit_hash:
                    commit['marked'] = True

        # Refresh the view
        self.commit_list.refresh_from_data()
    
    def return_to_mark(self):
        if self.marked_commit:
            for index, item in enumerate(self.commit_list.data):
                if item['commit_hash'] == self.marked_commit:
                    self.commit_list.commits.scroll_to_index(index)

    #TODO this needs testing with big repo
    def find_common_descendant(self, commit_hash_1, commit_hash_2):
        """
        Use git commands to find the latest common descendant of two commits.
        """
        try:
            # Get the list of all commits reachable from commit_hash_1 (reverse chronological order)
            result_1 = subprocess.run(
                ['git', 'rev-list', commit_hash_1],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result_1.returncode != 0:
                print(f"Error retrieving commits for {commit_hash_1}: {result_1.stderr}")
                return None

            # Get the list of all commits reachable from commit_hash_2 (reverse chronological order)
            result_2 = subprocess.run(
                ['git', 'rev-list', commit_hash_2],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result_2.returncode != 0:
                print(f"Error retrieving commits for {commit_hash_2}: {result_2.stderr}")
                return None

            # Convert the output to lists of commit hashes (chronological order)
            descendants_1 = result_1.stdout.splitlines()
            descendants_2 = result_2.stdout.splitlines()

            # Reverse both lists so that the latest commits come first
            descendants_1.reverse()
            descendants_2.reverse()

            # Find the latest common descendant (the last matching commit in both histories)
            for commit in descendants_1:
                if commit in descendants_2:
                    for index, item in enumerate(self.commit_list.data):
                        if item['commit_hash'] == commit:
                            self.commit_list.commits.select_item_by_index(index)
                            print(f"Latest common descendant: {commit}")

        except Exception as e:
            print(f"Error finding common descendant: {e}")
            return None

    def get_git_root(self):
        """
        Get the root directory of the current Git repository.
        """
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error finding Git root: {result.stderr}")
            return None
    
    def get_next_patch_filename(self, git_root):
        """
        Generate the next patch file name based on existing patch files in the git root.
        Sequential naming like patch0.patch, patch1.patch, etc.
        """
        patch_number = 0
        existing_files = os.listdir(git_root)

        # Check for existing patch files and find the highest number
        for filename in existing_files:
            if filename.startswith("patch") and filename.endswith(".patch"):
                try:
                    number = int(filename[5:-6])  # Extract the number between "patch" and ".patch"
                    if number >= patch_number:
                        patch_number = number + 1
                except ValueError:
                    pass  # Ignore files that don't follow the naming pattern

        # Return the next patch filename
        return f"patch{patch_number}.patch"
    
    def make_patch_popup(self, from_commit, to_commit):
        """
        Open the popup to generate the patch from the selected commit to the clicked commit,
        with an option to reverse the commits.
        """
        # Get the root directory of the Git repository
        git_root = self.get_git_root()
        if git_root is None:
            print("Could not find Git root directory.")
            return

        # Get commit messages for from_commit and to_commit
        from_commit_message = subprocess.run(
            ['git', 'log', '--format=%B', '-n', '1', from_commit],
            stdout=subprocess.PIPE,
            text=True
        ).stdout.strip()

        to_commit_message = subprocess.run(
            ['git', 'log', '--format=%B', '-n', '1', to_commit],
            stdout=subprocess.PIPE,
            text=True
        ).stdout.strip()
        popup = CustomPopup()
        # Create the layout for the popup
        

        # Commit from and to details
        b1 = BoxLayout()
        b1.add_widget(Label(text="From:",size_hint_x=None,width=40))
        from_commit_input = TextInput(text=f"{from_commit}\n{from_commit_message}",font_size=12, readonly=True, multiline=True)
        b1.add_widget(from_commit_input)
        popup.grid.add_widget(b1)

        b2 = BoxLayout()
        b2.add_widget(Label(text="To:",size_hint_x=None,width=40))
        to_commit_input = TextInput(text=f"{to_commit}\n{to_commit_message}",font_size=12, readonly=True, multiline=True)
        b2.add_widget(to_commit_input)
        popup.grid.add_widget(b2)

        # Reverse button
        reverse_button = Button(text="Reverse", size_hint=(1, None), height=40)
        reverse_button.bind(on_release=lambda x: self.reverse_commits(from_commit_input, to_commit_input))
        popup.grid.add_widget(reverse_button)

        # Get the next patch file name (patch0.patch, patch1.patch, etc.)
        next_patch_filename = self.get_next_patch_filename(git_root)

        # Default output file to Git root with sequential filename
        popup.grid.add_widget(Label(text="Output file:",size_hint_x=None,width=80))
        output_file_input = TextInput(text=f"{git_root}/{next_patch_filename}", multiline=False)
        popup.grid.add_widget(output_file_input)


        # Bind Generate button to action
        popup.ok_button.text = 'Generate'
        popup.ok_button.bind(on_release=lambda x: self.generate_patch(from_commit_input.text.split()[0],
                                                                    to_commit_input.text.split()[0],
                                                                    output_file_input.text))

        # Open the popup
        popup.open()

    def reverse_commits(self, from_input, to_input):
        """
        Swap the content of 'From' and 'To' commit inputs to reverse the patch generation.
        """
        from_text = from_input.text
        to_text = to_input.text

        # Swap the inputs
        from_input.text = to_text
        to_input.text = from_text

    def generate_patch(self, from_commit, to_commit, output_file):
        """
        Generate the patch between two commits and save it to the specified file.
        """
        try:
            # Generate the patch between the two commits
            result = subprocess.run(
                ['git', 'format-patch', f'{from_commit}..{to_commit}', '-o', output_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                print(f"Error generating patch: {result.stderr}")
            else:
                print(f"Patch saved at {output_file}")

        except Exception as e:
            print(f"Error generating patch: {e}")
         
    def cherry_pick_commit(self, commit_hash):
        """
        Show a popup to confirm cherry-picking the commit.
        Check if the commit is already in the current branch.
        """
        # Check if the commit is already in the current branch
        popup = CustomPopup(title="Cherry-pick Commit")
        popup.height = 200
        if self.is_commit_in_branch(commit_hash):
            # Show a popup to ask the user if they want to reapply the commit
            popup.info_lbl.text=f"Commit {commit_hash} is already in the current branch. Do you want to reapply it?"
            popup.ok_button.text="Reapply Commit"
            # Define what happens when the user decides to reapply
            popup.ok_button.bind(on_release=lambda x: self.execute_cherry_pick(commit_hash))
        else:
            # If the commit is not already in the branch, proceed with the regular cherry-pick confirmation
            popup.info_lbl.text=f"Cherry-pick commit: {commit_hash}"
            popup.ok_button.text="Cherry-pick"
            # Define what happens when cherry-pick is confirmed
            popup.ok_button.bind(on_release=lambda x: self.execute_cherry_pick(commit_hash))
        popup.open()

    def is_commit_in_branch(self, commit_hash):
        """
        Check if the given commit hash is already in the current branch.
        Returns True if the commit is already in the branch, False otherwise.
        """
        try:
            result = subprocess.run(
                ['git', 'branch', '--contains', commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # If the current branch is listed in the result, the commit is already in the branch
            return 'HEAD' in result.stdout or result.stdout.strip() != ""
        except Exception as e:
            print(f"Error checking commit in branch: {e}")
            return False

    def execute_cherry_pick(self, commit_hash):
        """
        Perform the cherry-pick operation for the given commit hash.
        """
        try:
            result = subprocess.run(
                ['git', 'cherry-pick', commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"Cherry-pick successful: {commit_hash}")
            else:
                print(f"Error during cherry-pick: {result.stderr}")
        except Exception as e:
            print(f"Exception during cherry-pick: {e}")

    def revert_commit(self, commit_hash):
        """
        Show a popup to confirm reverting the commit.
        """
        popup = CustomPopup(title="Revert Commit")
        popup.height = 200
        popup.info_lbl.text=f"Revert commit: {commit_hash}"
        popup.ok_button.text="Revert"
        popup.open()

    def execute_revert(self, commit_hash):
        """
        Perform the revert operation for the given commit hash.
        """
        try:
            result = subprocess.run(
                ['git', 'revert', commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"Revert successful: {commit_hash}")
                self.get_git_log(self.command_history[self.current_index],add_to_history=False)
            else:
                print(f"Error during revert: {result.stderr}")
        except Exception as e:
            print(f"Exception during revert: {e}")
    
    def reset_branch(self, commit_hash):
        """
        Show a popup to confirm resetting the branch.
        """
        popup = CustomPopup(title="Reset Branch")
        popup.height = 200
        popup.info_lbl.text = f"Reset branch to commit: {commit_hash}"

        # Create the reset type selection layout (soft, mixed, hard)
        reset_type_layout = BoxLayout(size_hint_y=None, height=40)

        soft_button = ToggleButton(text="Soft", group='reset', state='down')  # Default selected
        mixed_button = ToggleButton(text="Mixed", group='reset')
        hard_button = ToggleButton(text="Hard", group='reset')

        reset_type_layout.add_widget(soft_button)
        reset_type_layout.add_widget(mixed_button)
        reset_type_layout.add_widget(hard_button)

        popup.grid.add_widget(reset_type_layout)

        # Define what happens when reset is confirmed
        def execute_reset_action(instance):
            # Determine the selected reset type
            if soft_button.state == 'down':
                reset_type = 'soft'
            elif mixed_button.state == 'down':
                reset_type = 'mixed'
            elif hard_button.state == 'down':
                reset_type = 'hard'

            # Call execute_reset with the commit_hash and selected reset_type
            self.execute_reset(commit_hash, reset_type)

        # Bind the reset action to the ok_button
        popup.ok_button.bind(on_release=execute_reset_action)

        popup.open()

    #TODO needs testing
    def execute_reset(self, commit_hash, reset_type):
        """
        Perform the reset operation (soft, mixed, or hard) for the given commit hash.
        """
        try:
            # Run the git reset command with the selected reset type
            result = subprocess.run(
                ['git', 'reset', f'--{reset_type}', commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"Reset ({reset_type}) successful to commit: {commit_hash}")
                self.get_git_log(self.command_history[self.current_index],add_to_history=False)
            else:
                print(f"Error during reset: {result.stderr}")
        except Exception as e:
            print(f"Exception during reset: {e}")

    def create_tag_for_commit(self, commit_hash):
        """
        Show a popup to create a tag for the given commit without checking for existing tags.
        """
        popup = CustomPopup(title="Create Tag")
        popup.height = 250
        popup.info_lbl.text = f"Create a tag for commit: {commit_hash}"

        # Create a layout for tag input and tag type (annotated or lightweight)
        tag_layout = BoxLayout(orientation='vertical', spacing=10)

        # TextInput for tag name
        tag_input = TextInput(hint_text="Enter tag name", size_hint_y=None, height=40)
        tag_layout.add_widget(tag_input)

        # Radio buttons for tag types (annotated, lightweight)
        tag_type_layout = BoxLayout(size_hint_y=None, height=40)
        tag_type = 'annotated'  # Default tag type

        annotated_button = ToggleButton(text="Annotated", group='tag', state='down')  # Default selected
        lightweight_button = ToggleButton(text="Lightweight", group='tag')

        def set_tag_type(button):
            nonlocal tag_type
            tag_type = button.text.lower()

        annotated_button.bind(on_release=lambda x: set_tag_type(annotated_button))
        lightweight_button.bind(on_release=lambda x: set_tag_type(lightweight_button))

        tag_type_layout.add_widget(annotated_button)
        tag_type_layout.add_widget(lightweight_button)

        tag_layout.add_widget(tag_type_layout)
        popup.grid.add_widget(tag_layout)

        # Define what happens when tag creation is confirmed
        def execute_tag_creation(instance):
            tag_name = tag_input.text.strip()

            if not tag_name:
                print("Tag name cannot be empty.")
                return

            # Create the tag (no existence check needed)
            self.create_git_tag(commit_hash, tag_name, tag_type)

        # Bind the action to the ok_button
        popup.ok_button.bind(on_release=execute_tag_creation)

        popup.open()

    def create_git_tag(self, commit_hash, tag_name, tag_type):
        """
        Perform the tag creation for the given commit with the specified tag type (annotated or lightweight).
        """
        try:
            # Determine the command based on the tag type
            if tag_type == 'annotated':
                result = subprocess.run(
                    ['git', 'tag', '-a', tag_name, commit_hash, '-m', f"Tagging commit {commit_hash}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:  # Lightweight tag
                result = subprocess.run(
                    ['git', 'tag', tag_name, commit_hash],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

            if result.returncode == 0:
                print(f"Tag '{tag_name}' created successfully on commit {commit_hash}.")
            else:
                print(f"Error during tag creation: {result.stderr}")
        except Exception as e:
            print(f"Exception during tag creation: {e}")

    def create_branch_for_commit(self, commit_hash):
        """
        Show a popup to create a branch for the given commit, with UI refresh after branch creation.
        """
        popup = CustomPopup(title="Create Branch")
        popup.height = 200
        popup.info_lbl.text = f"Create a branch for commit: {commit_hash}"

        # Create a layout for branch input
        branch_layout = BoxLayout(orientation='vertical', spacing=10)

        # TextInput for branch name
        branch_input = TextInput(hint_text="Enter branch name", size_hint_y=None, height=40)
        branch_layout.add_widget(branch_input)

        popup.grid.add_widget(branch_layout)

        # Define what happens when branch creation is confirmed
        def execute_branch_creation(instance):
            branch_name = branch_input.text.strip()

            if not branch_name:
                print("Branch name cannot be empty.")
                return

            # Create the branch
            self.create_git_branch(commit_hash, branch_name)

            # Refresh the UI
            self.get_git_log(self.command_history[self.current_index],add_to_history=True)

        # Bind the action to the ok_button
        popup.ok_button.bind(on_release=execute_branch_creation)

        popup.open()

    def create_git_branch(self, commit_hash, branch_name):
        """
        Perform the branch creation for the given commit.
        """
        try:
            result = subprocess.run(
                ['git', 'branch', branch_name, commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                print(f"Branch '{branch_name}' created successfully from commit {commit_hash}.")
            else:
                print(f"Error during branch creation: {result.stderr}")
        except Exception as e:
            print(f"Exception during branch creation: {e}")
            
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view, but restricts to one item being selected. '''

    def __init__(self, **kwargs):
        super(SelectableRecycleBoxLayout, self).__init__(**kwargs)
        # Bind key events only when the widget is focused
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # Only handle the key down if the RecycleView (or its children) are focused
        if self.focus:
            if key == 273:  # Up arrow key
                self.move_selection(-1)
            elif key == 274:  # Down arrow key
                self.move_selection(1)

    #TODO might need a delay, so recycler stays with it
    def move_selection(self, direction):
        '''Moves the selection by direction (-1 for up, 1 for down), scrolling manually if the item is not visible.'''
        current_selection = self.selected_nodes[0] if self.selected_nodes else None
        if current_selection is not None:
            new_index = current_selection + direction
            if 0 <= new_index < len(self.parent.data):
                # Clear previous selection and select the new item
                self.clear_selection()
                self.select_node(new_index)

                # Attempt to get the widget representing the new index if it is currently visible
                view = self.parent.view_adapter.get_visible_view(index=new_index)
                
                if view:
                    scroll_up = False
                    # Get the position of the view in window coordinates
                    view_x, view_y = view.to_window(view.x, view.y)
                    view_top = view.to_window(view.x, view.top)[1]

                    # Get the top and bottom bounds of the RecycleView in window coordinates
                    rv_top = self.parent.to_window(self.parent.x, self.parent.top)[1]
                    rv_bottom = self.parent.to_window(self.parent.x, self.parent.y)[1]

                    # Check if the view is outside the visible bounds and calculate the distance
                    if view_top > rv_top:  # Scroll up
                        scroll_up = True
                    elif view_y < rv_bottom:  # Scroll down
                        scroll_up = False
                    else:
                        # The item is already visible; no scrolling needed
                        return

                    # Convert the distance to scroll units
                    _, scroll_y = self.parent.convert_distance_to_scroll(0, view.height)
                    
                    if scroll_up:  # Item is above the visible area; scroll up
                        if self.parent.scroll_y - scroll_y >= 1:
                            print('scroll up')
                            self.parent.scroll_y = self.parent.scroll_y - scroll_y
                        else:
                            self.parent.scroll_y = 1

                    elif not scroll_up:  # Item is below the visible area; scroll down
                        if self.parent.scroll_y - scroll_y >= 0:
                            print('scroll down')
                            self.parent.scroll_y = self.parent.scroll_y - scroll_y
                        else:
                            self.parent.scroll_y = 0
                else:
                    self.scroll_to_index(new_index)                
                    
    def scroll_to_index(self, index):
        ''' Scroll the RecycleView to ensure the selected item is visible '''
        total_items = len(self.parent.data)
        if total_items > 0:
            # Handle the special case where total_items is 1 to avoid division by zero
            if total_items == 1:
                scroll_y_position = 0  # With only one item, scroll to the top position
            else:
                # Scroll position is calculated as a percentage of the item index in the total list
                scroll_y_position = 1 - (index / (total_items - 1))
                
            self.parent.scroll_y = scroll_y_position  # Corrected to use self.parent (ScrollView)

    def select_item_by_index(self, index):
        ''' Select an item by index programmatically '''
        if 0 <= index < len(self.parent.data):  # Ensure the index is within bounds
            self.clear_selection()  # Clear any previous selection
            self.select_node(index)  # Select the node at the given index
            self.scroll_to_index(index)  # Scroll to the selected item

class FileLabel(Label):
    selected = BooleanProperty(False)
    file = StringProperty('')
    path = StringProperty('')
    bg_color = ListProperty([0, 0, 0])
    def __init__(self,root_widget=None, **kwargs):
        self.root_widget = root_widget
        self.long_touch_timer = None
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                return False

            # Handle right-click (desktop) by showing the context menu
            if touch.button == 'right':
                self.open_context_menu(touch)
            else:
                # Schedule long touch detection (1 second threshold)
                self.long_touch_timer = Clock.schedule_once(lambda dt: self.open_context_menu(touch), 1)
            return True
        
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        # If there's an active long-touch timer, cancel it and process the touch as a short touch
        if self.long_touch_timer:
            self.long_touch_timer.cancel()
            self.long_touch_timer = None
            
            # Trigger normal selection if it wasn't a long touch
            if not self.selected:
                self.selected = True
            else:
                self.selected = False
        
        return super().on_touch_up(touch)
    
    def open_context_menu(self, touch):
        # Cancel any ongoing long touch timer to avoid further action
        if self.long_touch_timer:
            self.long_touch_timer.cancel()
            self.long_touch_timer = None

        # Create a DropDown menu
        dropdown = CustomDropdown()

        context_options = [
            ('highlight this too', lambda: self.root_widget.highlight_commits_for_file(self.path,True)),
            ('highlight this only', lambda: self.root_widget.highlight_commits_for_file(self.path,False)),
            ('copy path', lambda: self.copy_path_to_clipboard()),
            #('external diff', lambda: self.root_widget.revert_commit(self.commit_hash)),
            ('blame parent commit', lambda: self.root_widget.blame_parent_commit(self.path)),
        ]

        # Add options to the dropdown
        for option_text, option_action in context_options:
            btn = CustomDropBtn(text=option_text)
            btn.bind(on_release=lambda btn, action=option_action: [dropdown.dismiss(), action()])
            dropdown.add_widget(btn)

        # Convert touch coordinates to window coordinates
        win_x, win_y = self.to_window(*touch.pos)

        # Create a temporary floating widget at the touch position
        floating_widget = Widget(size=(0, 0))  # Widget of size 0,0
        floating_widget.pos = (win_x, win_y)

        # Add the floating widget directly to the Window
        Window.add_widget(floating_widget)

        # Open the dropdown on the floating widget
        dropdown.open(floating_widget)
        dropdown.auto_width = False
        dropdown.width = 200

        # After opening the dropdown, remove the floating widget since it's no longer needed
        def remove_floating_widget(*args):
            Window.remove_widget(floating_widget)

        # Set a trigger to remove the floating widget after dropdown closes
        dropdown.bind(on_dismiss=remove_floating_widget)
    
    def copy_path_to_clipboard(self):
        """Copy the file path to the clipboard."""
        Clipboard.copy(self.path)

    def on_selected(self, *args):
        if self.selected:
            for file in self.root_widget.tree_box.children:
                if file != self:
                    file.selected = False
                    
            text_content = self.root_widget.diff_scroll.text
            search_text = f"diff --git a/{self.path} b/{self.path}"

            # Find the position of the search_text in the content
            file_start_index = text_content.find(search_text)

            if file_start_index != -1:
                # Calculate the number of lines before the file start index
                preceding_text = text_content[:file_start_index]
                row = preceding_text.count('\n')

                # Set the cursor to the bottom (resetting the scroll to the last line)
                total_lines = text_content.count('\n')
                self.root_widget.diff_scroll.cursor = (0, total_lines)  # Set cursor to the last line

                # Now set the cursor to the start of the line where the file begins
                Clock.schedule_once(lambda dt: self.root_widget.move_cursor_to_row(row))  # delay to allow gui update

            self.bg_color = (.12, .12, .12)
        else:
            self.bg_color = (0, 0, 0)

class TreeLabel(Label, TreeViewNode):
    selected = BooleanProperty(False)
    file = StringProperty('')
    path = StringProperty('')
    bg_color = ListProperty([0, 0, 0])

    def __init__(self, file='', path='', root_widget=None, **kwargs):
        super(TreeLabel, self).__init__(**kwargs)
        self.file = file
        self.path = path
        self.root_widget = root_widget

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                return False

            # Handle right-click (desktop) by showing the context menu
            if touch.button == 'right':
                self.open_context_menu(touch)
            return True
        
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # Ensure this event only processes if the touch is inside this widget's boundaries
        if self.collide_point(*touch.pos):
            self.root_widget.on_file_click(self.path)
            return super().on_touch_up(touch)
        
        # If the touch didn't collide with this widget, call the parent's on_touch_up
        return super().on_touch_up(touch)
    
    def open_context_menu(self, touch):
        dropdown = CustomDropdown()

        context_options = [
            ('highlight this too', lambda: self.root_widget.highlight_commits_for_file(self.path,True)),
            ('highlight this only', lambda: self.root_widget.highlight_commits_for_file(self.path,False)),
            ('copy path', lambda: self.copy_path_to_clipboard()),
            #('external diff', lambda: self.root_widget.(self.commit_hash)),
            ('blame parent commit', lambda: self.root_widget.blame_parent_commit(self.path)),
        ]

        # Add options to the dropdown
        for option_text, option_action in context_options:
            btn = CustomDropBtn(text=option_text)
            btn.bind(on_release=lambda btn, action=option_action: [dropdown.dismiss(), action()])
            dropdown.add_widget(btn)

        # Convert touch coordinates to window coordinates
        win_x, win_y = self.to_window(*touch.pos)

        # Create a temporary floating widget at the touch position
        floating_widget = Widget(size=(0, 0))  # Widget of size 0,0
        floating_widget.pos = (win_x, win_y)

        # Add the floating widget directly to the Window
        Window.add_widget(floating_widget)

        # Open the dropdown on the floating widget
        dropdown.open(floating_widget)
        dropdown.auto_width = False
        dropdown.width = 200

        # After opening the dropdown, remove the floating widget since it's no longer needed
        def remove_floating_widget(*args):
            Window.remove_widget(floating_widget)

        # Set a trigger to remove the floating widget after dropdown closes
        dropdown.bind(on_dismiss=remove_floating_widget)

    def copy_path_to_clipboard(self):
        """Copy the file path to the clipboard."""
        Clipboard.copy(self.path)

class CommitLine(RecycleDataViewBehavior, BoxLayout):
    selected = BooleanProperty(False)
    highlighted = BooleanProperty(False)
    marked = BooleanProperty(False)  
    graph = StringProperty("")
    commit_hash = StringProperty("")
    message = StringProperty("")
    author = StringProperty("")
    date = StringProperty("")
    graph_lenght = NumericProperty(0)

    def refresh_view_attrs(self, rv, index, data):
        ''' Refresh the view with new data from the RV '''
        self.index = index
        self.highlighted = data.get('highlighted', False)  # Reset highlighted state based on data
        self.marked = data.get('marked', False)  # Reset highlighted state based on data
        self.graph_lenght = data.get('graph_lenght', 0)
        return super(CommitLine, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(CommitLine, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.open_context_menu(touch)
                return True
            else:
                return self.parent.select_with_touch(self.index, touch)

    def open_context_menu(self, touch):
        # Create a DropDown menu
        dropdown = CustomDropdown()
        
        # Define context menu options, calling root widget's methods with commit hash
        context_options = []
        app = App.get_running_app()
        # only add diff options if selection if found and the clicked one is not same as the selection

        # Check if there's a selection and it's not the current commit
        if app.root.selection and app.root.selection != self.commit_hash:
            context_options.append(('diff this -> selected', lambda: app.root.diff_commits(self.commit_hash, app.root.selection), False))
            context_options.append(('diff selected -> this', lambda: app.root.diff_commits(app.root.selection, self.commit_hash), False))
            context_options.append(('make patch', lambda: app.root.make_patch_popup(app.root.selection, self.commit_hash), False))
        else:
            # Still add the options but mark them as disabled
            context_options.append(('diff this -> selected', None, True))
            context_options.append(('diff selected -> this', None, True))
            context_options.append(('make patch', None, True))

        context_options.append(('mark this commit', lambda: app.root.mark_commit(self.commit_hash), False))

        # Check if there's a marked commit and it's not the current commit
        if app.root.marked_commit and app.root.marked_commit != self.commit_hash:
            context_options.append(('return to mark', lambda: app.root.return_to_mark(), False))
            context_options.append(('find descendant of this and mark', lambda: app.root.find_common_descendant(self.commit_hash, app.root.marked_commit), False))
            context_options.append(('diff this -> marked', lambda: app.root.diff_commits(self.commit_hash, app.root.marked_commit), False))
            context_options.append(('diff marked -> this', lambda: app.root.diff_commits(app.root.marked_commit, self.commit_hash), False))
        else:
            # Add the options but mark them as disabled
            context_options.append(('return to mark', None, True))
            context_options.append(('find descendant of this and mark', None, True))
            context_options.append(('diff this -> marked', None, True))
            context_options.append(('diff marked -> this', None, True))

        context_options.append(('cherry-pick this commit', lambda: app.root.cherry_pick_commit(self.commit_hash), False))
        context_options.append(('revert this commit', lambda: app.root.revert_commit(self.commit_hash), False))
        context_options.append(('reset branch to this commit', lambda: app.root.reset_branch(self.commit_hash), False))
        context_options.append(('create tag', lambda: app.root.create_tag_for_commit(self.commit_hash), False))
        context_options.append(('create branch', lambda: app.root.create_branch_for_commit(self.commit_hash), False))

        # Add options to the dropdown
        for option_text, option_action, is_disabled in context_options:
            btn = CustomDropBtn(text=option_text, disabled=is_disabled)
            if option_action:
                btn.bind(on_release=lambda btn, action=option_action: [dropdown.dismiss(), action()])
            dropdown.add_widget(btn)

        # Convert touch coordinates to window coordinates
        win_x, win_y = self.to_window(*touch.pos)

        # Create a temporary floating widget at the touch position
        floating_widget = Widget(size=(0, 0))
        floating_widget.pos = (win_x, win_y)

        # Add the floating widget directly to the Window
        Window.add_widget(floating_widget)

        # Open the dropdown on the floating widget
        dropdown.open(floating_widget)
        dropdown.auto_width = False
        dropdown.width = 200

        # After opening the dropdown, remove the floating widget since it's no longer needed
        def remove_floating_widget(*args):
            Window.remove_widget(floating_widget)

        # Set a trigger to remove the floating widget after dropdown closes
        dropdown.bind(on_dismiss=remove_floating_widget)
  
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            # Get reference to MainWidget through App and set selection
            app = App.get_running_app()
            app.root.selection = self.commit_hash

    def get_plain_text_length(self, text):
        """Removes Kivy markup tags and whitespace, then returns the length of plain text."""
        # Remove markup tags (anything inside square brackets)
        plain_text = re.sub(r'\[.*?\]', '', text)
        # Remove all whitespace (spaces, tabs, newlines)
        plain_text = re.sub(r'\s+', '', plain_text)
        return len(plain_text)

from kivy.modules import inspector
class siGitApp(App):
    
    def __init__(self, parsed_args, **kwargs):
        super().__init__(**kwargs)
        self.parsed_args = parsed_args

    def build(self):
        # Load the KV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        Builder.load_file(os.path.join(current_dir, 'main.kv'))
        main_widget = MainWidget(parsed_arguments=self.parsed_args)
        inspector.create_inspector(Window, main_widget)
        return main_widget

def parse_arguments():
    """
    Parse command-line arguments for flexibility with git log.
    Accepts any valid git log arguments in free-form.
    """
    parser = argparse.ArgumentParser(description="Run git log with optional arguments")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments passed to git log (e.g., master, --since=2023-01-01)")
    parsed_args = parser.parse_args()
    return parsed_args.args

def main():
    # Parse free-form arguments
    arguments = parse_arguments()
    # Run the Kivy app, passing in the parsed arguments
    siGitApp(arguments).run()

if __name__ == '__main__':
    main()
    