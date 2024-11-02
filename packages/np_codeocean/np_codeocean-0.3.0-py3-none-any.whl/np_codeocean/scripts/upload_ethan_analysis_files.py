import upath
import concurrent.futures
local_to_s3_mapping = {
    "//allen/programs/mindscope/workgroups/dynamicrouting/Ethan/new_annotations/single unit metrics": "s3://aind-scratch-data/dynamic-routing/ethan/single-unit-metrics",
    "//allen/programs/mindscope/workgroups/templeton/TTOC/decoding results/": "s3://aind-scratch-data/dynamic-routing/ethan/decoding-results",
}

def helper(local_root, s3_root, file):
    s3_path = upath.UPath(s3_root) / file.relative_to(local_root)
    if not file.is_file():
        return 
    if s3_path.exists():
        print(file.relative_to(local_root), " - already uploaded")
        return
    print(file.relative_to(local_root))
    s3_path.write_bytes(file.read_bytes())
        
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for local_root, s3_root in local_to_s3_mapping.items():
            for file in upath.UPath(local_root).rglob("*"):
                executor.submit(helper, local_root, s3_root, file)
