import subprocess
import re
import pandas as pd
from shutil import which


def git_is_available():
    """Check whether `git` is on PATH

    Returns:
        bool: True if, `git` binary is on path
    """
    if which("git"):
        return True
    else:
        return False


def get_authors_from_git(path_to_repo):
    cmd = f"git -C {path_to_repo} log --format='%an <%ae>'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return list(set(result.stdout.splitlines()))


def get_coauthors_from_git(path_to_repo):
    """ Collect declared co-authors from all commit messages """
    cmd = f"git -C {path_to_repo} log --format='%B'"
    all_commit_msgs = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    co_authors = []

    results = re.findall(
        r"^Co-authored-by: ((?:\w|\-| ){0,38}) <(\S*)>$",
        all_commit_msgs,
        re.MULTILINE,
    )
    for author in results:
        co_authors.append(f"{author[0]} <{author[1]}>")

    return co_authors


def _convert_authors_str_to_df(authors):
    df = pd.DataFrame(authors, columns=["authors_orig"])

    names_and_mails = df.authors_orig.apply(split_author_info).tolist()
    df[["author_name", "author_email"]] = pd.DataFrame(
        names_and_mails, index=df.index, columns=["author_name", "author_email"]
    )

    return df


def _group_by_emails(df):
    return df.groupby("author_email").agg(list).reset_index()


def _convert_name_lst_to_str(df):
    # Make a string out of the author names again
    def get_first(lst):
        return lst[0]

    mask = df.author_name.apply(len) == 1
    name_strs = df[mask].author_name.apply(get_first)
    df.loc[mask, "author_name"] = name_strs

    return df


def _group_by_names(df):
    def flatten(lst):
        return [inner_el for el in lst for inner_el in el]

    _convert_name_lst_to_str(df)

    mask = df.author_name.apply(type) == str
    same_name_df = df[mask].groupby("author_name").agg(list)  # TODO: include similarity measure here

    if same_name_df.empty:
        return df
    else:
        same_name_df.authors_orig = same_name_df.authors_orig.apply(flatten)

        mask = df.author_name.apply(type) == list
        for idx, row in df[mask].iterrows():
            for author_name in row.author_name:
                try:
                    # TODO: include similarity measure here
                    same_name_df.loc[author_name].authors_orig += df.iloc[idx].authors_orig
                except KeyError:
                    continue
        return same_name_df


def _create_mailmap_df(df):
    mailmap_rows = []
    for _, row in df.iterrows():
        author_map_idx = row.authors_orig[0]
        author_aliases = row.authors_orig[1:]
        if author_aliases:
            for author_alias in author_aliases:
                mailmap_rows.append((author_map_idx, author_alias))
        else:
            mailmap_rows.append((author_map_idx, ""))

    mailmap_df = pd.DataFrame(mailmap_rows, columns=("author", "author_alias")).drop_duplicates()
    return mailmap_df


def compute_mailmap(authors):
    """Rules:

    - authors with same email address are one person
    - authors with same name but different email addresses are one person <- might be wrong
    - authors with similar names and different email addresses are one person <- might be really wrong, e.g. for short names
    """
    df = _convert_authors_str_to_df(authors)
    # Stage One - Grouping on exact same email addresses
    same_mail_df = _group_by_emails(df)

    # Stage Two - Grouping on exact same names and combination with email grouping
    same_name_df = _group_by_names(same_mail_df)

    # Stage Three - Grouping on similar names and combination with email grouping
    # Not implemented yet...
    #   - Implement it either with SequenceMatcher from above
    #   - or use fuzzy string matching from [thefuzz](https://github.com/seatgeek/thefuzz/)
    #      - https://pythoninoffice.com/use-fuzzy-string-matching-in-pandas/
    #      - https://python.plainenglish.io/all-the-fuzzyness-of-python-72d12d094195
    return _create_mailmap_df(same_name_df)


def mailmap_df_to_str(df):
    result_str = ""
    for _, row in df.iterrows():
        result_str += f"{row.author} {row.author_alias}\n"
    return result_str


def split_author_info(author_str):
    author_name, author_email = author_str.split(" <")
    author_email = author_email[:-1]

    return author_name, author_email


def create_mailmap(paths_to_repos):
    authors = []
    for path_to_repo in paths_to_repos:
        authors += get_authors_from_git(path_to_repo)
        authors += get_coauthors_from_git(path_to_repo)
    mailmap = compute_mailmap(set(authors))
    mailmap_str = mailmap_df_to_str(mailmap)
    return mailmap_str
