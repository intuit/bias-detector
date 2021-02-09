import re

from bias_detector.common import *
from bias_detector.fuzzy_names_from_emails.FullName import FullName

import nltk

nltk.download('words')
nltk.download('wordnet')


class FuzzyEmailFullNameExtractor:

    def __init__(self) -> None:
        self.emails_full_names_functions = [self.get_email_full_name_using_sep,
                                            self.get_email_first_name_perfect_match,
                                            self.get_email_last_name_perfect_match,
                                            self.get_email_full_name_perfect_match,
                                            self.get_email_full_name_perfect_match_reversed,
                                            self.get_email_last_name_near_perfect_match,
                                            self.get_email_first_name_near_perfect_match]
                                            # self.get_email_first_name_where_last_name_not_found,
                                            # self.get_email_last_name_where_first_name_not_found]
        self.words_set = set(nltk.corpus.words.words())

    def fuzzily_get_email_full_name(self, email: str) -> FullName:
        email = email.lower()
        email_prefix = email.split(sep='@', maxsplit=1)[0]
        cleaned = re.sub(r'(?:^[\d]+)|(?:[+.\-_\d]+$)', '', email_prefix)
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemma = lemmatizer.lemmatize(cleaned)
        if lemma in self.words_set:
            return FullName('', '')
        for func in self.emails_full_names_functions:
            full_name = func(cleaned)
            if full_name is not None and not full_name.is_empty():
                return full_name
        return FullName('', '')

    def get_email_full_name_using_sep(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        split = re.split(r'[+.\-_\d]+', prefix)
        if len(split) > 1:
            first_name_candidate = re.sub(r'(?:^[\d]+)|(?:[\d]+$)', '', split[0])
            if first_name_candidate in all_first_names_set:
                first_name = first_name_candidate
            last_name_candidate = re.sub(r'(?:^[\d]+)|(?:[\d]+$)', '', split[-1])
            if last_name_candidate in all_last_names_set:
                last_name = last_name_candidate
            full_name = FullName(first_name, last_name)
            if not full_name.is_full():
                full_name_reversed = self.get_email_full_name_using_sep_reversed(prefix)
                if full_name_reversed.is_full():
                    return full_name_reversed
                else:
                    return full_name
        return FullName(first_name, last_name)

    def get_email_full_name_using_sep_reversed(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        split = re.split(r'[+.\-_\d]+', prefix)
        if len(split) > 1:
            first_name_candidate = re.sub(r'(?:^[\d]+)|(?:[\d]+$)', '', split[1])
            if first_name_candidate in all_first_names_set:
                first_name = first_name_candidate
            last_name_candidate = re.sub(r'(?:^[\d]+)|(?:[\d]+$)', '', split[0])
            if last_name_candidate in all_last_names_set:
                last_name = last_name_candidate
        return FullName(first_name, last_name)

    def get_email_full_name_perfect_match(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        for i in range(len(prefix) - 3, 2, -1):
            if prefix[:i] in all_first_names_set and prefix[i:] in all_last_names_set:
                first_name = prefix[:i]
                last_name = prefix[i:]
                break
        return FullName(first_name, last_name)

    def get_email_full_name_perfect_match_reversed(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        for i in range(len(prefix) - 3, 2, -1):
            if prefix[:i] in all_last_names_set and prefix[i:] in all_first_names_set:
                first_name = prefix[i:]
                last_name = prefix[:i]
                break
        return FullName(first_name, last_name)

    def get_email_first_name_perfect_match(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        if prefix in all_first_names_set:
            first_name = prefix
        return FullName(first_name, last_name)

    def get_email_last_name_perfect_match(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        if prefix in all_last_names_set:
            last_name = prefix
        return FullName(first_name, last_name)

    def get_email_last_name_near_perfect_match(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        candidate = '' if len(prefix) < 4 else prefix[1:]
        if candidate in all_last_names_set:
            last_name = candidate
        return FullName(first_name, last_name)

    def get_email_first_name_near_perfect_match(self, prefix: str) -> FullName:
        first_name = ''
        last_name = ''
        candidate = '' if len(prefix) < 4 else prefix[:-1]
        if candidate in all_first_names_set:
            first_name = candidate
        return FullName(first_name, last_name)

    # def get_email_first_name_where_last_name_not_found(self, prefix: str) -> FullName:
    #     first_name = ''
    #     last_name = ''
    #     split = re.split(r'[.\-_]', prefix)
    #     if len(split) > 1:
    #         return FullName(first_name, last_name)
    #     for i in range(len(prefix) - 4, 3, -1):
    #         if prefix[:i] in all_first_names_set:
    #             first_name = prefix[:i]
    #             break
    #     return FullName(first_name, last_name)

    # def get_email_last_name_where_first_name_not_found(self, prefix: str) -> FullName:
    #     first_name = ''
    #     last_name = ''
    #     split = re.split(r'[.\-_]', prefix)
    #     if len(split) > 1:
    #         return FullName(first_name, last_name)
    #     for i in range(4, len(prefix) - 4):
    #         if prefix[i:] in all_last_names_set:
    #             last_name = prefix[i:]
    #             break
    #     return FullName(first_name, last_name)
