import mmap
import bisect

def find_start_offset(file_path, target_time):
    with open(file_path, 'rb') as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        start, end = 0, len(mmapped_file)

        while start < end:
            mid = (start + end) // 2

            # Move to the start of the line
            while mid > 0 and mmapped_file[mid] != ord('\n'):
                mid -= 1
            if mid > 0:
                mid += 1

            # Read the log line
            line_start = mid
            line_end = mmapped_file.find(b'\n', mid)
            if line_end == -1:
                break

            line = mmapped_file[line_start:line_end].decode()
            parts = line.split(" ", 2)
            if len(parts) < 3:
                start = mid + 1
                continue

            timestamp = parts[0]

            if timestamp >= target_time:
                return mid  # Found approximate position

            start = line_end + 1

        return None  # Timestamp not found


# Example Usage
file_path = r"C:\Users\HP\Downloads\logs_2024.log\logs_2024.log"
start_time = "2024-01-01T00:00:00"
offset = find_start_offset(file_path, start_time)
print(f"Start offset: {offset}")

