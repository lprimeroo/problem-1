from pydriller import RepositoryMining
from tqdm import tqdm
import lizard
from collections import defaultdict

class ArgumentCommits():
  def __init__(self, urls=[]):
    self.mining_object = RepositoryMining(urls, only_in_main_branch=True, only_modifications_with_file_types=['.java'])
    self.commit_records = defaultdict(list)
    self.result = ''

  def fetch_commit_data(self):
    for commit in self.mining_object.traverse_commits():
      for mod in commit.modifications:
        if mod.filename[-5:] == '.java':
          commit_code_details = lizard.analyze_file.analyze_source_code(mod.filename, mod.source_code)

          for func in commit_code_details.function_list:
            d = func.__dict__
            self.commit_records[f'{mod.filename}~{["name"]}'].append({
              'hash': commit.hash,
              'current_signature': d["long_name"],
              'args': d["parameters"]})

  def find_commits_with_additional_parameters(self):
    print("Fetching commits and running static analysis: In Progress...")
    self.fetch_commit_data()
    print("Fetching commits and running static analysis: Done!")
    print("Finding Commits with Additional Parameters: In Progress...")
    for key, value in self.commit_records.items():
      file_name = key.split('~')[0]
      l = len(value)
      for i in range(0, l - 1):
        if len(value[i + 1]['args']) > len(value[i]['args']):
          self.result += f'{value[i + 1]["hash"]},{file_name},{value[i]["current_signature"]},{value[i + 1]["current_signature"]}\n'
        
    print("Finding Commits with Additional Parameters: Done!")


  def write_to_csv(self, filename="default_file_name"):
    with open(f'{filename}.csv', 'w') as file:
      file.write('Commit SHA,Java File,Old function signature,New function signature\n')
      for line in self.result:
        file.write(line)