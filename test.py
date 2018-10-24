from argument_commits import ArgumentCommits

c = ArgumentCommits(urls=['https://github.com/ReactiveX/RxJava'])
c.find_commits_with_additional_parameters()
c.write_to_csv(filename='./Examples/RxJava')