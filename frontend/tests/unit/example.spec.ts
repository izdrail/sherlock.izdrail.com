import { mount } from '@vue/test-utils';
import { describe, expect, test } from 'vitest';
import RawRirDataEventCard from '@/views/reports/cards/RawRirDataEventCard.vue';
import EmailAddrCompromisedEventCard from '@/views/reports/cards/EmailAddrCompromisedEventCard.vue';

describe('RawRirDataEventCard.vue', () => {
  test('parses Python dictionary string and displays key-value pairs', () => {
    const rawPythonData = "{'first_name': 'Damien', 'last_name': 'Geery', 'venmo_id': '418668'}";
    const wrapper = mount(RawRirDataEventCard, {
      props: {
        event: {
          event_type: 'RAW_RIR_DATA',
          source_data: 'Venmo API',
          last_seen: '2024-12-01',
          data: rawPythonData
        }
      }
    });

    const text = wrapper.text();
    expect(text).toContain('First Name');
    expect(text).toContain('Damien');
    expect(text).toContain('Last Name');
    expect(text).toContain('Geery');
    expect(text).toContain('Venmo Id');
    expect(text).toContain('418668');
  });
});

describe('EmailAddrCompromisedEventCard.vue', () => {
  test('consolidates compromised events and extracts websites', () => {
    const events = [
      {
        event_type: 'EMAILADDR_COMPROMISED',
        source_data: 'HIBP',
        last_seen: '2024-12-01',
        data: 'dgeery@gmail.com [brandnewtube.com]'
      },
      {
        event_type: 'EMAILADDR_COMPROMISED',
        source_data: 'HIBP',
        last_seen: '2024-12-01',
        data: 'dgeery@gmail.com [adobe.com]'
      }
    ];

    const wrapper = mount(EmailAddrCompromisedEventCard, {
      props: { events }
    });

    const text = wrapper.text();
    expect(text).toContain('Compromised Accounts');
    expect(text).toContain('2 Findings');
    expect(text).toContain('brandnewtube.com');
    expect(text).toContain('adobe.com');
  });
});
