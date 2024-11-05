import os
import torch
import numpy as np
import pandas as pd

import warnings

class Network_analyzer():
    def __init__(self,noise_threshold=1e-5):
        warnings.warn("Network visualization is performed using R, "
                      "this function only calculate the z-score matrix of significant "
                      "CCI network for each sample", UserWarning)

        # load data
        print("Start loading data")
        self.noise_threshold=noise_threshold
        result_dir = os.path.join(os.getcwd(), "influence_tensor")
        if result_dir[-1] != "/":
            result_dir = result_dir + "/"
        self.result_dir=result_dir
        data_dir = os.path.join(os.getcwd(), "data", "processed")
        if data_dir[-1] != "/":
            data_dir = data_dir + "/"
        cell_types = torch.load(os.path.join(os.getcwd(), "data", "processed", "cell_types.pth"))
        self.cell_types = cell_types
        genes = torch.load(os.path.join(os.getcwd(), "data", "genes.pth"))
        self.genes = genes

        cell_type_pair_sequence = []
        for cell_typei in cell_types:
            for cell_typej in cell_types:
                cell_type_pair_sequence.append(cell_typei + "__" + cell_typej)
        self.cell_type_pair_sequence=cell_type_pair_sequence

        if not os.path.exists(os.path.join(os.getcwd(), "network")):
            os.mkdir(os.path.join(os.getcwd(), "network"))
        if not os.path.exists(os.path.join(os.getcwd(), "network", "significant_network")):
            os.mkdir(os.path.join(os.getcwd(), "network", "significant_network"))
        if not os.path.exists(os.path.join(os.getcwd(), "network", "interaction_strength")):
            os.mkdir(os.path.join(os.getcwd(), "network", "interaction_strength"))
        if not os.path.exists(os.path.join(os.getcwd(), "network", "counts")):
            os.mkdir(os.path.join(os.getcwd(), "network", "counts"))
        # Get sample names
        samples = []
        for filei in os.listdir(data_dir):
            if filei.find("_TypeExp.npz") >= 0:
                samples.append(filei.split("_TypeExp.npz")[0])
        self.samples = list(sorted(list(set(samples))))
        print("Finish loading data")

    def reshape_z_value(self,result_dict):
        results = []
        for genei in self.genes + ["all"]:
            resulti = np.zeros((len(self.cell_type_pair_sequence)))
            tmp = result_dict[genei]
            for j in range(len(tmp[0])):
                resulti[self.cell_type_pair_sequence.index(tmp[0][j])] = tmp[1][j]
            results.append(resulti)
        return np.stack(results, axis=0).transpose((-1, -2))  # (number_of_cell_type_pair,genes)

    def determine_network_sample(self,sample):
        # Load the results
        results = torch.load(self.result_dir + "edges_" + sample + ".pth")

        # Extract relevant data
        attention_scores = results["attention_score"]  # Shape (B, 49, C)
        proportion = torch.abs(attention_scores)
        proportion = proportion / torch.sum(proportion, dim=1, keepdim=True)
        attention_scores[proportion < self.noise_threshold] = 0

        cell_type_names = np.array(results["cell_type_name"])  # Shape (B, 50)
        true_expression = results["y"]  # Shape (B, C)
        # print(calculate_mean_expression_by_cell_type(true_expression, cell_type_names[:,0], cell_types))

        # Initialize a tensor to hold aggregated interaction strengths
        B, _, C = attention_scores.shape
        t = len(self.cell_types)
        aggregated_interactions = torch.zeros((B, t, C))

        # Map cell type names to indices
        cell_type_to_index = {ct: idx for idx, ct in enumerate(self.cell_types)}

        # Aggregate interaction strengths by cell type
        for b in range(B):
            for n in range(1, 50):  # Skip the first element, which is the target cell type
                neighbor_type = cell_type_names[b][n]
                if neighbor_type in cell_type_to_index:
                    idx = cell_type_to_index[neighbor_type]
                    aggregated_interactions[b, idx] += attention_scores[b, n - 1]

        aggregated_interactions = torch.abs(aggregated_interactions) / torch.sum(torch.abs(aggregated_interactions),
                                                                                 dim=1, keepdim=True)

        # Prepare to compute correlations for each cell type pair
        results_matrix = []

        for pair in self.cell_type_pair_sequence:
            from_type, to_type = pair.split("__")
            if from_type in cell_type_to_index:
                mask = (cell_type_names[:, 0] == to_type)
                filtered_interactions = aggregated_interactions[mask, cell_type_to_index[from_type]]
                filtered_expressions = true_expression[mask]
                if np.sum(mask) == 0:
                    results_matrix.append([0 for k in range(C)])
                    continue

                # Calculate Pearson correlation coefficient for each gene
                corr_coeffs = []
                for i in range(C):
                    gene_interactions = filtered_interactions[:, i]
                    gene_expressions = filtered_expressions[:, i]
                    if len(gene_interactions) <= 10 or ((gene_interactions == gene_interactions[0]).all() or (
                            gene_expressions == gene_expressions[0]).all()):
                        corr_coeffs.append(0)
                        continue
                    r = torch.corrcoef(torch.stack((gene_interactions, gene_expressions)))[0, 1]
                    n = gene_interactions.numel()
                    z_value = r * ((n - 2) ** 0.5) / (1 - r ** 2) ** 0.5
                    if torch.isnan(z_value) or torch.isinf(z_value) or r == 1:
                        print(from_type, to_type, np.sum((cell_type_names[:, 0] == to_type)))
                        print(r, z_value, gene_interactions, gene_expressions)
                        z_value = 0
                    corr_coeffs.append(float(z_value))
                results_matrix.append(corr_coeffs)

        # Convert results to a tensor of shape (t^2, C)
        results_matrix = np.array(results_matrix)
        results_matrix = np.nan_to_num(results_matrix)
        df = pd.DataFrame(data=results_matrix, columns=self.genes, index=self.cell_type_pair_sequence)
        df.to_csv(os.path.join(os.getcwd(), "network", "significant_network",sample + ".csv"))
        return results_matrix

    def get_counts_sample(self,sample):
        results = torch.load(self.result_dir + "edges_" + sample + ".pth")
        cell_type_name = results["cell_type_name"]
        cell_type_target = [cell_type_name[i][0] for i in range(len(cell_type_name))]
        types, counts = np.unique(cell_type_target, return_counts=True)
        counts = counts.tolist()
        types = types.tolist()
        counts1 = []
        for i in range(len(self.cell_types)):
            if self.cell_types[i] not in types:
                print(self.cell_types[i], "not in", sample, "with cell types:", types)
                counts1.append(0)
                continue
            counts1.append(counts[types.index(self.cell_types[i])])
        df = pd.DataFrame({"cell_type": self.cell_types, "counts": counts1})
        df.to_csv(os.path.join(os.getcwd(), "network", "counts", sample + ".csv"), index=False)

    def get_counts(self):
        for samplei in self.samples:
            self.get_counts_sample(samplei)

    def determine_networks(self):
        for samplei in self.samples:
            self.determine_network_sample(samplei)







