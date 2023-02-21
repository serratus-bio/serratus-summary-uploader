# worker
from batch.rdrp.aurora import RdrpBatch


run_ids = ('ERR004293', 'ERR239333', 'ERR239334', 'ERR2393982')
rdrp_batch = RdrpBatch(run_ids, log_id='test')
rdrp_batch.download()
rdrp_batch.parse()
rdrp_batch.create_dataframes()


def test_tables():
    assert list(rdrp_batch.tables.keys()) == ['sra', 'phy', 'fam', 'vir']


def test_sra():
    table = rdrp_batch.tables['sra']
    assert list(table.entries[0].keys()) == ['run_id', 'read_length', 'genome', 'aligned_reads', 'truncated', 'date']
    assert list(table.df.columns) == ['run_id', 'read_length', 'genome', 'aligned_reads', 'date', 'truncated']


def test_phy():
    table = rdrp_batch.tables['phy']
    assert table.entries[0]['coverage_bins'] == '_________________._______'
    assert table.entries[0]['phy'] == 'pisu'
    assert table.entries[0]['score'] == 2
    assert table.entries[0]['percent_identity'] == 50
    assert table.entries[0]['depth'] == 0.1
    assert table.entries[0]['n_reads'] == 1
    assert table.entries[0]['aligned_length'] == 26
    assert table.entries[0]['run_id'] == 'DRR015317'
    assert table.entries[0]['phylum_name'] == 'Pisuviricota'


def test_fam():
    table = rdrp_batch.tables['fam']
    assert table.entries[0]['coverage_bins'] == '_________________._______'
    assert table.entries[0]['fam'] == 'pisu.Unc159'
    assert table.entries[0]['score'] == 2
    assert table.entries[0]['percent_identity'] == 50
    assert table.entries[0]['depth'] == 0.1
    assert table.entries[0]['n_reads'] == 1
    assert table.entries[0]['aligned_length'] == 26
    assert table.entries[0]['run_id'] == 'DRR015317'
    assert table.entries[0]['phylum_name'] == 'Pisuviricota'
    assert table.entries[0]['family_name'] == 'Unclassified-159'
    assert table.entries[0]['family_group'] == 'Unc159'
    assert table.entries[1]['coverage_bins'] == '__.______________________'
    assert table.entries[1]['fam'] == 'kiti.Tombusviridae-14'
    assert table.entries[1]['score'] == 1
    assert table.entries[1]['percent_identity'] == 67
    assert table.entries[1]['depth'] == 0.0
    assert table.entries[1]['n_reads'] == 1
    assert table.entries[1]['aligned_length'] == 21
    assert table.entries[1]['run_id'] == 'DRR015317'
    assert table.entries[1]['phylum_name'] == 'Kitrinoviricota'
    assert table.entries[1]['family_name'] == 'Tombusviridae'
    assert table.entries[1]['family_group'] == 'Tombusviridae-14'


def test_vir():
    table = rdrp_batch.tables['vir']
    assert table.entries[0]['coverage_bins'] == '_________________._______'
    assert table.entries[0]['vir'] == 'pisu.Unc159.picalivirus_c:AFR11839'
    assert table.entries[0]['score'] == 2
    assert table.entries[0]['percent_identity'] == 50
    assert table.entries[0]['depth'] == 0.1
    assert table.entries[0]['n_reads'] == 1
    assert table.entries[0]['aligned_length'] == 26
    assert table.entries[0]['run_id'] == 'DRR015317'
    assert table.entries[0]['virus_name'] == 'picalivirus_c'
    assert table.entries[0]['sequence_accession'] == 'AFR11839'
    assert table.entries[0]['phylum_name'] == 'Pisuviricota'
    assert table.entries[0]['family_name'] == 'Unclassified-159'
    assert table.entries[0]['family_group'] == 'Unc159'
