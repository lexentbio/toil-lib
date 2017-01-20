import os

from toil.lib.docker import dockerCall

from toil_lib.files import tarball_files


def run_fastqc(job, r1_id, r2_id):
    """
    Run Fastqc on the input reads

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param str r1_id: FileStoreID of fastq read 1
    :param str r2_id: FileStoreID of fastq read 2
    :return: FileStoreID of fastQC output (tarball)
    :rtype: str
    """
    work_dir = job.fileStore.getLocalTempDir()
    job.fileStore.readGlobalFile(r1_id, os.path.join(work_dir, 'R1.fastq'))
    parameters = ['/data/R1.fastq']
    output_names = ['R1_fastqc.html', 'R1_fastqc.zip']
    if r2_id:
        job.fileStore.readGlobalFile(r2_id, os.path.join(work_dir, 'R2.fastq'))
        parameters.extend(['-t', '2', '/data/R2.fastq'])
        output_names.extend(['R2_fastqc.html', 'R2_fastqc.zip'])
    dockerCall(job=job, tool='quay.io/ucsc_cgl/fastqc:0.11.5--be13567d00cd4c586edf8ae47d991815c8c72a49',
               workDir=work_dir, parameters=parameters)
    output_files = [os.path.join(work_dir, x) for x in output_names]
    tarball_files(tar_name='fastqc.tar.gz', file_paths=output_files, output_dir=work_dir)
    return job.fileStore.writeGlobalFile(os.path.join(work_dir, 'fastqc.tar.gz'))
