#
#   Dataset sampling functionality
#   Tanguy Ophoff
#

def stratified_splits(df, split_percentages, *, class_column=None, stratify_columns=None):
    """
    This function splits a dataset in N stratified splits.
    If a `class_column` is given, each class is split independently and the subsplits are combined afterwards, ensuring a similar distribution in each split.
    This class column can be tought of as the most important stratum, for which the distribution must be adhered to.
    Other columns passed to `stratify_columns` are fed through a DBSCAN algorithm to compute clusters which are used as subgroups when splitting.

    Args:
        df (pandas.DataFrame): The dataset that needs to be split
        split_percentages (list[float]): The different split percentages (needs to sum to 1)
        class_column (str, optional): The name of the column representing the classes (or most important stratum); Default None
        stratify_column (list[str], optional): The names of columns that need to be taken into account for equal splits; Default None

    Returns:
        (list[list[int]]): The indices in each split

    Required Libraries:
        pandas
        scikit-learn

    Example:
        >>> df = ...
        >>> train_idx, test_idx = stratified_splits(df, [0.8, 0.2], class_column='class_label', stratify_columns=['width', 'height'])
    """
    import math
    import random
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    
    assert sum(split_percentages) == 1, 'All splits combined should be 100% of the data'
    df = df.copy()
    
    # Assign constant class if none is given
    if class_column is None:
        class_column = 'stratsplit-klass_col'
        df[class_column] = 0
        
    # Loop through classes and split each class in N stratified splits
    splits = [[] for _ in range(len(split_percentages))]
    total = 0
    for _, group in df.groupby(class_column, observed=True):
        if stratify_columns is not None:
            features = StandardScaler().fit_transform(group[stratify_columns])
            group['stratsplit-stratum'] = DBSCAN().fit_predict(features)
        else:
            group['stratsplit-stratum'] = 0
        
        for _, subgroup in group.groupby('stratsplit-stratum'):
            indices = tuple(subgroup.index.tolist())
            X = len(indices)
            counts = [s * len(indices) for s in split_percentages[:-1]]
            if total > 0:
                counts = [
                    math.ceil(c) if len(splits[idx]) / total < split_percentages[idx] else math.floor(c)
                    for idx, c in enumerate(counts)
                ]
            else:
                counts = [math.floor(c) for c in counts]

            for idx, c in enumerate(counts):
                chosen_idx = random.sample(indices, k=min(len(indices), c))
                splits[idx].extend(chosen_idx)
                indices = tuple(i for i in indices if i not in chosen_idx)
            splits[-1].extend(indices)
            
            total += subgroup.shape[0]
    
    assert sum(len(s) for s in splits) == df.shape[0], 'All elements should be chosen'
    return splits
