print("""# Load required libraries
if (!require("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c("DESeq2", "pasilla"))

library(DESeq2)
library(pasilla)
library(ggplot2)

# Load count and metadata
cts <- as.matrix(read.csv(system.file("extdata", "pasilla_gene_counts.tsv", package="pasilla"), sep="\t", row.names="gene_id"))
coldata <- read.csv(system.file("extdata", "pasilla_sample_annotation.csv", package="pasilla"), row.names=1)
coldata$condition <- factor(coldata$condition)
rownames(coldata) <- sub("fb", "", rownames(coldata))
cts <- cts[, rownames(coldata)]  # Ensure matching order

# Differential Expression Analysis
dds <- DESeqDataSetFromMatrix(countData=cts, colData=coldata, design=~condition)
dds <- DESeq(dds)
res <- results(dds)
write.csv(res, "DESeq_Analysis.csv")

# Load results and label differential expression
df <- read.csv("DESeq_Analysis.csv")
df$Diffexpressed <- ifelse(df$log2FoldChange > 0.1 & df$pvalue < 0.05, "UP", 
                           ifelse(df$log2FoldChange < -0.1 & df$pvalue < 0.05, "DOWN", "NO"))

# Plot volcano plot
ggplot(df, aes(x=log2FoldChange, y=-log10(pvalue), color=Diffexpressed)) +
  geom_vline(xintercept=c(-1, 1), col="black", linetype="dashed") +
  geom_vline(xintercept=c(-0.5, 0.5), col="green", linetype="dashed") +
  geom_hline(yintercept=-log10(0.00003), col="red", linetype="dashed") +
  geom_hline(yintercept=-log10(0.05), col="black", linetype="dashed") +
  geom_point(size=2) +
  theme_minimal() +
  scale_color_manual(values=c("DOWN"="#00AFBB", "NO"="grey", "UP"="pink")) +
  labs(title="Volcano Plot", x="log2(Fold Change)", y="-log10(p-value)")

# Export upregulated and downregulated gene lists
write(rownames(df[df$Diffexpressed == "UP", ]), "upreg.txt")
write(rownames(df[df$Diffexpressed == "DOWN", ]), "downreg.txt")""")


