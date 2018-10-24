from argument_commits import ArgumentCommits

c = ArgumentCommits(urls=['https://github.com/zxing/zxing'])
c.find_commits_with_additional_parameters()
c.write_to_csv(filename='./Samples/ZXing')
c.write_to_tsv(filename='./Samples/ZXing')