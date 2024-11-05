def read_10x_mtx(
    path: Path | str,
    *,
    var_names: Literal["gene_symbols", "gene_ids"] = "gene_symbols",
    make_unique: bool = True,
    cache: bool = False,
    cache_compression: Literal["gzip", "lzf"] | None | Empty = _empty,
    gex_only: bool = True,
    prefix: str | None = None,
) -> AnnData:
    """\
    Read 10x-Genomics-formatted mtx directory.

    Parameters
    ----------
    path
        Path to directory for `.mtx` and `.tsv` files,
        e.g. './filtered_gene_bc_matrices/hg19/'.
    var_names
        The variables index.
    make_unique
        Whether to make the variables index unique by appending '-1',
        '-2' etc. or not.
    cache
        If `False`, read from source, if `True`, read from fast 'h5ad' cache.
    cache_compression
        See the h5py :ref:`dataset_compression`.
        (Default: `settings.cache_compression`)
    gex_only
        Only keep 'Gene Expression' data and ignore other feature types,
        e.g. 'Antibody Capture', 'CRISPR Guide Capture', or 'Custom'
    prefix
        Any prefix before `matrix.mtx`, `genes.tsv` and `barcodes.tsv`. For instance,
        if the files are named `patientA_matrix.mtx`, `patientA_genes.tsv` and
        `patientA_barcodes.tsv` the prefix is `patientA_`.
        (Default: no prefix)

    Returns
    -------
    An :class:`~anndata.AnnData` object
    """
    path = Path(path)
    prefix = "" if prefix is None else prefix
    is_legacy = (path / f"{prefix}genes.tsv").is_file()
    adata = _read_10x_mtx(
        path,
        var_names=var_names,
        make_unique=make_unique,
        cache=cache,
        cache_compression=cache_compression,
        prefix=prefix,
        is_legacy=is_legacy,
    )
    if is_legacy or not gex_only:
        return adata
    gex_rows = adata.var["feature_types"] == "Gene Expression"
    return adata[:, gex_rows].copy()


def _read_10x_mtx(
    path: Path,
    *,
    var_names: Literal["gene_symbols", "gene_ids"] = "gene_symbols",
    make_unique: bool = True,
    cache: bool = False,
    cache_compression: Literal["gzip", "lzf"] | None | Empty = _empty,
    prefix: str = "",
    is_legacy: bool,
) -> AnnData:
    """
    Read mex from output from Cell Ranger v2- or v3+
    """
    suffix = "" if is_legacy else ".gz"
    adata = read(
        path / f"{prefix}matrix.mtx{suffix}",
        cache=cache,
        cache_compression=cache_compression,
    ).T  # transpose the data
    genes = pd.read_csv(
        path / f"{prefix}{'genes' if is_legacy else 'features'}.tsv{suffix}",
        header=None,
        sep="\t",
    )
    if var_names == "gene_symbols":
        var_names_idx = pd.Index(genes[1].values)
        if make_unique:
            var_names_idx = anndata.utils.make_index_unique(var_names_idx)
        adata.var_names = var_names_idx
        adata.var["gene_ids"] = genes[0].values
    elif var_names == "gene_ids":
        adata.var_names = genes[0].values
        adata.var["gene_symbols"] = genes[1].values
    else:
        raise ValueError("`var_names` needs to be 'gene_symbols' or 'gene_ids'")
    if not is_legacy:
        adata.var["feature_types"] = genes[2].values
    barcodes = pd.read_csv(path / f"{prefix}barcodes.tsv{suffix}", header=None)
    adata.obs_names = barcodes[0].values
    return adata
