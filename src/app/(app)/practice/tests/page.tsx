import { redirect } from 'next/navigation';

// The tests index used to list several test engines. There is now one test
// screen with three kinds of test, so this address simply leads there.
export default function TestsIndexPage() {
  redirect('/test');
}
