import re

class InterestingPaths(object):

    def __init__(self):
        self._include_patterns = []
        self._exclude_patterns = []

    def mark_path_as_interesting(self, path):
        self._include_patterns.append(re.compile(path))

    def mark_path_as_boring(self, path):
        self._exclude_patterns.append(re.compile(path))

    def is_interesting(self, path):
        rooted_path = '/' + path
        included = len(self._include_patterns) == 0
        if not included:
            for pre in self._include_patterns:
                if pre.match(rooted_path):
                    included = True
                    break
        if included:
            for pre in self._exclude_patterns:
                if pre.match(rooted_path):
                    included = False
                    break
        return included

    def get_interesting_sub_directories(self, path):
        if len(path) == 0 or self.is_interesting(path):
            return [path]
        return [ ]
