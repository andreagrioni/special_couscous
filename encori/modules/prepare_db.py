import pandas as pd
import os


def combine_df(main_df, supp_df, how="inner"):
    """
    function combines encori and mirna df.
    return overlapping df.

    paramenters:
    main_df=encori df
    supp_df=mirna df
    how=method (def. inner)
    """
    return main_df.merge(supp_df, how=how, on="miRNAid")


def clean_annotation(annotation_path, biotype):
    """
    filter annotation for specific 
    biotype(s) and return pandas df

    parameters:
    annotation_path=path to annotation GTF file
    biotype=list of biotype names

    """

    header = "chrom,source,biotype,start,end,score,strand,phase,info".split(",")

    df = pd.read_csv(annotation_path, sep="\t", comment="#", header=None, names=header)
    df_filtered = df[df["biotype"].isin(biotype)].copy().reset_index(drop=True)
    return df_filtered


def get_mask(file_path):
    """
    load repeat mask bed track
    as pandas df.

    paramenters:
    file_path=path to bed file
    """
    col_names = "chrom,start,end,name,score,strand".split(",")
    df_mask = pd.read_csv(file_path, sep="\t", header=None, names=col_names,)
    return df_mask


def load_db(annotation, biotype, repeat_mask):
    """
    wrapper of above functions, returns pandas df
    of annotation, repeat mask, and encori db
    
    paramenters:
    annotation=path to gtf annotation
    biotype=list of biotypes
    repeat_mask=path to repeat mask
    encori_path=path to encori db
    """

    df_anno = clean_annotation(annotation, biotype)
    df_mask = get_mask(repeat_mask)

    return df_anno, df_mask


if __name__ == "__main__":
    print("testing clean_annotation()")
    repeat_mask = "./data/repeat_mask_hg19.bed"
    anno_path, biotype = "./data/toy_gencode.gtf", ["UTR"]
    df_anno, df_mask = load_db(anno_path, biotype, repeat_mask)
    print(df_anno.head(10))
    print(df_mask.head(10))
