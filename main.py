"""SCD Type 2 Customer History. Synthetic portfolio demonstration."""
from datetime import date

def run(data):
    history = []
    for change in sorted(data['changes'], key=lambda r:(r['at'],r['customer'])):
        date.fromisoformat(change['at'])
        current = next((r for r in history if r['customer']==change['customer'] and r['to'] is None), None)
        if current and current['region'] == change['region']:
            continue
        if current:
            if current['from'] == change['at']:
                raise ValueError('Conflicting changes at the same effective date')
            current['to'] = change['at']
        history.append({'customer':change['customer'],'region':change['region'],
                        'from':change['at'],'to':None})
    query = data['lookup']
    date.fromisoformat(query['at'])
    match = next((r for r in history if r['customer']==query['customer'] and
                  r['from'] <= query['at'] and (r['to'] is None or query['at'] < r['to'])), None)
    return {'history':history,'as_of_region':match['region'] if match else None}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
