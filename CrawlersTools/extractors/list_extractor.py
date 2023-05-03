#!/usr/bin/env python
# coding=utf-8
"""
Author: xiaobin.zhu
since: 2022-11-24 14:24:09
LastAuthor: xiaobin.zhu
LastEditTime: 2022-11-24 14:24:09
Description: extract list from index page
FilePath: list_extractor
"""
import math
import operator
from collections import defaultdict
from urllib.parse import urljoin

# from loguru import logger
import numpy as np
from lxml.html import fromstring

from CrawlersTools.extractors.base import BaseExtractor
from CrawlersTools.extractors.schemas.element import Element
from CrawlersTools.extractors.utils.cluster import cluster_dict
from CrawlersTools.extractors.utils.element import calc_a_descendants_text_of_avg_length, descendants_of_body
from CrawlersTools.extractors.utils.preprocess import preprocess4list_extractor
from CrawlersTools.extractors.utils.settings import (
    LIST_AVG_LENGTH, LIST_MAX_LENGTH, LIST_MIN_LENGTH, LIST_MIN_NUMBER, ADDTION_RIGHT_NUM, SIMILARITY_THRESHOLD,
    HIGH_WEIGHT_ERROR_KEYWORD, DIRECTORY_ERROR_TITLE, SPECIAL_SYMBOL_MAP,
)

AVG_LENGTH = (LIST_MIN_LENGTH + LIST_MAX_LENGTH) / 2


class ListExtractor(BaseExtractor):
    """
    extract list from index page
    """

    @staticmethod
    def _probability_of_title_with_length(length):
        """
        get the probability of title according to length
        import matplotlib.pyplot as plt
        x = np.asarray(range(5, 40))
        y = list_extractor.probability_of_title_with_length(x)
        plt.plot(x, y, 'g', label='m=0, sig=2')
        plt.show()
        :param length:
        :return:
        """
        sigma = 6
        return np.exp(-1 * ((length - AVG_LENGTH) ** 2) / (2 * (sigma**2))) / (
            math.sqrt(2 * np.pi) * sigma
        )

    @staticmethod
    def _build_clusters(element):
        """
        build candidate clusters according to element
        :return:
        """
        descendants = descendants_of_body(element)
        descendants_tree = defaultdict(list)
        for descendant in descendants:
            #  dispose some special descendant for less extract
            if len(descendant.a_descendants) > 5 and descendant.number_of_siblings == 1:
                if descendant.parent_selector in ["html>body", "html"]:
                    continue
                if descendant.a_descendants_group_text_min_length > LIST_MAX_LENGTH:
                    continue
                if descendant.a_descendants_group_text_max_length < LIST_MIN_LENGTH:
                    continue
                for link in descendant.a_descendants:
                    descendants_tree[descendant.parent_selector].append(link)
                continue
            # if one element does not have enough siblings, it can not become a child of candidate element
            if descendant.number_of_siblings + 1 < LIST_MIN_NUMBER:
                continue
            if calc_a_descendants_text_of_avg_length(descendant) < LIST_AVG_LENGTH:
                continue
            # if min length is larger than specified max length, it can not become a child of candidate element
            if descendant.a_descendants_group_text_min_length > LIST_MAX_LENGTH:
                continue
            # if max length is smaller than specified min length, it can not become a child of candidate element
            if descendant.a_descendants_group_text_max_length < LIST_MIN_LENGTH:
                continue
            # if descendant.a_descendants_group_text_avg_length < 10:
            #     continue
            # descendant element must have same siblings which their similarity should not below similarity_threshold
            if descendant.similarity_with_siblings < SIMILARITY_THRESHOLD:
                continue
            descendants_tree[descendant.parent_selector].append(descendant)
        if len(descendants_tree) == 0:
            return
        descendants_tree = dict(descendants_tree)

        # cut tree, remove parent block
        selectors = sorted(list(descendants_tree.keys()))
        last_selector = None
        for selector in selectors[::-1]:
            # if later selector
            if last_selector and selector and last_selector.startswith(selector):
                del descendants_tree[selector]
            last_selector = selector
        clusters = cluster_dict(descendants_tree)

        return clusters

    @staticmethod
    def _evaluate_cluster(cluster):
        """
        calculate score of cluster using similarity, numbers, or other info
        :param cluster:
        :return:
        """
        score = dict()

        # calculate avg_similarity_with_siblings
        score["avg_similarity_with_siblings"] = np.mean(
            [element.similarity_with_siblings for element in cluster]
        )
        score["avg_text_length"] = np.mean(
            [calc_a_descendants_text_of_avg_length(element) for element in cluster]
        )
        # calculate number of elements
        score["number_of_elements"] = len(cluster)

        score["clusters_score"] = (
            score["avg_similarity_with_siblings"]
            * np.log10(score["number_of_elements"] + 1)
            * score["avg_text_length"]
        )
        # * clusters_score[cluster_id]['probability_of_title_with_length']
        return score

    @staticmethod
    def _extend_cluster(cluster):
        """
        extend cluster's elements except for missed children
        :param cluster:
        :return:
        """
        result = [element.selector for element in cluster]
        for element in cluster:
            if calc_a_descendants_text_of_avg_length(element) < LIST_AVG_LENGTH:
                continue
            path_raw = element.path_raw
            siblings = list(element.siblings)
            for sibling in siblings:
                # skip invalid element
                if not isinstance(sibling, Element):
                    continue
                sibling_selector = sibling.selector
                sibling_path_raw = sibling.path_raw
                if sibling_path_raw != path_raw:
                    continue
                # add missed sibling
                if sibling_selector not in result:
                    cluster.append(sibling)
                    result.append(sibling_selector)

        cluster = sorted(cluster, key=lambda x: x.nth)
        # logger.debug(f"cluster after extend {cluster}")
        return cluster

    def _best_cluster(self, clusters):
        """
        use clustering algorithm to choose best cluster from candidate clusters
        :param clusters:
        :return:
        """
        if not clusters:
            # logger.debug("there is on cluster, just return empty result")
            return []
        if len(clusters) == 1:
            # logger.debug("there is only one cluster, just return first cluster")
            return clusters[0]
        # choose best cluster using score
        clusters_score = defaultdict(dict)
        clusters_score_arg_max = 0
        clusters_score_max = -1
        for cluster_id, cluster in clusters.items():
            if len(cluster) < 2:
                continue
            # calculate avg_similarity_with_siblings
            clusters_score[cluster_id] = self._evaluate_cluster(cluster)
            # get max score arg index
            if clusters_score[cluster_id]["clusters_score"] > clusters_score_max:
                clusters_score_max = clusters_score[cluster_id]["clusters_score"]
                clusters_score_arg_max = cluster_id
        # logger.debug(f"clusters_score {clusters_score}")
        best_cluster = clusters[clusters_score_arg_max]
        return best_cluster

    def _extract_cluster(self, cluster):
        """
        extract title and href from best cluster
        :param cluster:
        :return:
        """
        if not cluster:
            return None
        # get best tag path of title
        probabilities_of_title = defaultdict(list)
        for element in cluster:
            if element.tag == "a":
                descendants = [element]
            else:
                descendants = element.a_descendants
            for descendant in descendants:
                path = descendant.path_raw
                descendant_text = descendant.text
                probability_of_title_with_length = (
                    self._probability_of_title_with_length(len(descendant_text))
                )

                if descendant.attrib.get("title"):
                    probability_of_title_with_length = (
                        probability_of_title_with_length * ADDTION_RIGHT_NUM
                    )

                if len(descendant_text) > LIST_MAX_LENGTH:
                    probability_of_title_with_length = (
                        probability_of_title_with_length * ADDTION_RIGHT_NUM
                    )
                if (
                    descendant.tag == "a"
                    and descendant.get("parent")
                    and calc_a_descendants_text_of_avg_length(descendant.parent)
                    < LIST_AVG_LENGTH
                ):
                    probability_of_title_with_length = (
                        probability_of_title_with_length / ADDTION_RIGHT_NUM
                    )
                else:
                    if (
                        calc_a_descendants_text_of_avg_length(descendant)
                        < LIST_AVG_LENGTH
                    ):
                        probability_of_title_with_length = (
                            probability_of_title_with_length / ADDTION_RIGHT_NUM
                        )
                for ss in HIGH_WEIGHT_ERROR_KEYWORD:
                    if ss in descendant_text:
                        probability_of_title_with_length = (
                            probability_of_title_with_length / ADDTION_RIGHT_NUM
                        )

                probability_of_title = probability_of_title_with_length
                probabilities_of_title[path].append(probability_of_title)
        probabilities_of_title_bak = {}
        for key in probabilities_of_title:
            if len(probabilities_of_title[key]) > LIST_MIN_NUMBER - 2:
                probabilities_of_title_bak[key] = probabilities_of_title[key]
        probabilities_of_title = probabilities_of_title_bak
        # get most probable tag_path
        probabilities_of_title_avg = {
            k: np.mean(v) for k, v in probabilities_of_title.items()
        }
        if not probabilities_of_title_avg:
            return None
        best_path = max(probabilities_of_title_avg.items(), key=operator.itemgetter(1))[
            0
        ]
        # logger.debug(f"best tag path {best_path}")

        # extract according to best tag path
        result = []
        # 去除重复链接
        cache_url_list = []
        recode_avg_len_of_path = {}
        for element in cluster:
            avg_len = calc_a_descendants_text_of_avg_length(element)
            parent_selector = element.parent_selector
            if recode_avg_len_of_path.get(parent_selector) is not None:
                if recode_avg_len_of_path[parent_selector] < LIST_AVG_LENGTH:
                    continue
            else:
                recode_avg_len_of_path[parent_selector] = avg_len
                if recode_avg_len_of_path[parent_selector] < LIST_AVG_LENGTH:
                    continue

            if element.tag == "a":
                path_raw = element.path_raw
                if path_raw != best_path:  # and descendant.text == ""
                    continue
                title = element.attrib.get("title") or element.text
                if title in DIRECTORY_ERROR_TITLE or len(title) < 2:
                    continue
                flag = False
                for ss in HIGH_WEIGHT_ERROR_KEYWORD:
                    if ss in title:
                        flag = True
                        break
                if flag:
                    continue
                url = element.attrib.get("href")
                if url is None:
                    continue
                if "javascript" in url:
                    ss = element.attrib.get("data-href")
                    if ss is not None:
                        url = ss
                if "#" in url or "javascript:void" in url:
                    ss = element.attrib.get("onclick")
                    if ss is not None:
                        url = ss

                if url.startswith("//"):
                    url = "http:" + url
                base_url = self.kwargs.get("base_url")
                if base_url:
                    url = urljoin(base_url, url)
                if url in cache_url_list:
                    continue
                else:
                    cache_url_list.append(url)
                result.append({"title": title, "url": url})
                continue
            else:
                descendants = element.a_descendants
            for descendant in descendants:
                path_raw = descendant.path_raw
                if path_raw != best_path:  # and descendant.text == ""
                    continue
                title = descendant.attrib.get("title") or descendant.text
                if title in DIRECTORY_ERROR_TITLE or len(title) < 2:
                    continue
                flag = False
                for ss in HIGH_WEIGHT_ERROR_KEYWORD:
                    if ss in title:
                        flag = True
                        break
                if flag:
                    continue
                url = descendant.attrib.get("href")
                if url is None:
                    continue
                if "javascript" in url:
                    ss = descendant.attrib.get("data-href")
                    if ss is not None:
                        url = ss
                if "#" in url or "javascript:void" in url:
                    ss = descendant.attrib.get("onclick")
                    if ss is not None:
                        url = ss

                if url.startswith("//"):
                    url = "http:" + url
                base_url = self.kwargs.get("base_url")
                if base_url:
                    url = urljoin(base_url, url)
                if url in cache_url_list:
                    continue
                else:
                    cache_url_list.append(url)
                result.append({"title": title, "url": url})
        return result

    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        # preprocess
        preprocess4list_extractor(element)

        # build clusters
        clusters = self._build_clusters(element)
        # logger.debug(f"after build clusters {clusters}")

        # choose best cluster
        best_cluster = self._best_cluster(clusters)
        # logger.debug(f"best cluster {best_cluster}")

        extended_cluster = self._extend_cluster(best_cluster)
        # logger.debug(f"extended cluster {extended_cluster}")

        # extract result from best cluster
        return self._extract_cluster(best_cluster)

    def extract(self, html, **kwargs):
        self.kwargs = kwargs
        for key, value in SPECIAL_SYMBOL_MAP.items():
            html = html.replace(key, value)

        element = fromstring(html=html)  # html有多个，fromstring默认取第一个 TODO 解析不了非规范html
        if self.kwargs.get("list_xpath"):
            return ''.join(element.xpath(self.kwargs.get("list_xpath")))

        element.__class__ = Element
        return self.process(element)
