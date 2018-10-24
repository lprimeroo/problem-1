from pydriller import RepositoryMining
from dateutil.parser import parse
import lizard
from collections import defaultdict

class ArgumentCommits():
  def __init__(self, urls=[]):
    self.mining_object = RepositoryMining(urls, only_in_main_branch=True, only_modifications_with_file_types=['.java'])
    self.commit_records = defaultdict(list)
    self.result = ''

  def fetch_commit_data(self):
    '''
      This routine fetches the commit data of the specified repository
      and runs static analysis on the code files in the commit.
    '''
    for commit in self.mining_object.traverse_commits():
      for mod in commit.modifications:
        if mod.filename[-5:] == '.java': # get only Java files from the commit
          commit_code_details = lizard.analyze_file.analyze_source_code(mod.filename, mod.source_code)

          for func in commit_code_details.function_list:
            d = func.__dict__
            if 'for(' in d["long_name"]:  continue # handling the case where 'for()' is considered a function by lizard.

            self.commit_records[f'{mod.filename}~{d["name"]}'].append({
              'hash': commit.hash,
              'doc': commit.author_date.strftime("%Y-%m-%d %H:%M:%S"), # doc == date of commit
              'current_signature': d["long_name"],
              'args': d["parameters"]})

  def find_commits_with_additional_parameters(self):
    '''
      This routine finds the commits where one or more arguments was added to 
      a function.
    '''
    print("Fetching commits and running static analysis: In Progress...")
    self.fetch_commit_data()
    print("Fetching commits and running static analysis: Done!")
    print("Finding Commits with Additional Parameters: In Progress...")
    for key, value in self.commit_records.items():
      value.sort(key=lambda el: parse(el["doc"])) # sort the commits by date of commit
      file_name = key.split('~')[0]
      l = len(value)
      current_signature = value[0]['current_signature']

      for i in range(0, l - 1):
        if len(value[i + 1]['args']) > len(value[i]['args']) and value[i + 1]["current_signature"] != current_signature and value[i + 1]["hash"] != value[i]["hash"]:
          self.result += f'{value[i + 1]["hash"]},{file_name},{value[i]["current_signature"]},{value[i + 1]["current_signature"]}\n'
          current_signature = value[i + 1]["current_signature"]
        
    print("Finding Commits with Additional Parameters: Done!")


  def write_to_csv(self, filename="default_file_name"):
    with open(f'{filename}.csv', 'w') as file:
      file.write('Commit SHA,Java File,Old function signature,New function signature\n')
      for line in self.result:
        file.write(line)