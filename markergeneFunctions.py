# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:28:39 2023

@author: Jenyi

Functions for extracting marker genes from clusters by pairwise comparison
"""
import json
import numpy as np

def get_gene_stats_by_cluster(data_arr, 
					 cluster_labels, 
					 clusters):
	
	"""
	GEt statistics for each cluster and each gene.
	Parameters:
		data_arr: (# of samples, # of genes) numpy array
			 Array of data points
		 cluster_labels: numpy array
			 Cluster labels for each point
		 clusters: list
			 List of clusters
	 Returns:
		median_arr: (# of cluster, # of genes) numpy array
			   Array of median values for each cluster and each gene
	   mean_arr: (# of cluster, # of genes) numpy array
			   Array of mean values for each cluster and each gene		 
	
	
	"""

	median_arr = np.zeros((len(clusters), data_arr.shape[1]))
	mean_arr = np.zeros_like(median_arr)
# 	var_arr = np.zeros_like(mean_arr)
	
	for n in range(len(clusters)):
		cluster_arr = data_arr[cluster_labels==clusters[n]]
		mean_arr[n, :] = np.mean(cluster_arr, axis=0)
		median_arr[n, :] = np.median(cluster_arr, axis=0)	
# 		var_arr[n, :] = np.var(cluster_arr, axis=0)
		
	return median_arr, mean_arr


def filter_genes_by_median(median_arr, mean_arr):	
	"""
	Get marker genes using the median expression >2 times other clusters and mean CPM counts > 1.
	
	Parameters:
		median_arr: (# of cluster, # of genes) numpy array
			   Array of median values for each cluster and each gene
	   mean_arr: (# of cluster, # of genes) numpy array
			   Array of mean values for each cluster and each gene
			   
   Returns:
	   None

	"""

	cluster_dict = {}
	marker_rank_dict = {}		
	for n in range(len(mean_arr)):
		cluster_dict[n] = []
		marker_rank_dict[n] = []		
	for n in range(mean_arr.shape[1]):
		top_cluster = np.argmax(median_arr[:, n])
		if mean_arr[top_cluster, n] >= 1:
		    median_exp = median_arr[top_cluster, n]
		    temp_median_arr = median_arr[:, n]
		    temp_median_arr = np.delete(temp_median_arr, top_cluster, axis=0)
		    if np.all(temp_median_arr*2 < median_exp):
		        cluster_dict[top_cluster].append(n)
		        marker_rank_dict[top_cluster].append(median_exp/np.mean(temp_median_arr))

	#sort markers by fold change over mean
	for n in cluster_dict.keys():
		a = cluster_dict[n]
		b = marker_rank_dict[n]
		sorted_genes = [x for _, x in sorted(zip(b, a))]
		sorted_fold_change = sorted(b)
		cluster_dict[n] = sorted_genes
		marker_rank_dict[n] = sorted_fold_change
				
	#save sorted arrays
	with open('marker_genes.json', 'w') as f:
	    json.dump(cluster_dict, f)
	with open('marker_genes_fc.json', 'w') as f:
	    json.dump(marker_rank_dict, f)		
		
	return

def plot_marker_genes(n_genes:int=10):
	
	
		
	