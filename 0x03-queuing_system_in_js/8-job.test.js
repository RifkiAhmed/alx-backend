const kue = require('kue');
const { expect } = require('chai');
const sinon = require('sinon');
const createPushNotificationsJobs = require('./8-job');


describe('createPushNotificationsJobs', () => {
  let queue;
  let consoleSpy;
  const jobs = [
    {
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account'
    },
    {
      phoneNumber: '4153518781',
      message: 'This is the code 4562 to verify your account'
    }
  ];

  beforeEach(() => {
    queue = kue.createQueue();
    consoleSpy = sinon.spy(console, 'log');
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    consoleSpy.restore();
  });

  it('createPushNotificationsJob throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('createPushNotificationsJobs create a job for each item in the jobs array', () => {
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
  });

  it('createPushNotificationsJobs log a message when a job is created', () => {
    createPushNotificationsJobs(jobs, queue);
    expect(consoleSpy.calledWithMatch(/Notification job created: .+/)).to.be.true;
  });

  it('createPushNotificationsJobs adds jobs to an array in memory', () => {
    createPushNotificationsJobs(jobs, queue);
    const job_1 = queue.testMode.jobs[0];
    const job_2 = queue.testMode.jobs[1];
    expect(job_1.type).to.equal('push_notification_code_3');
    expect(job_1.data).to.deep.equal(jobs[0]);
    expect(job_2.type).to.equal('push_notification_code_3');
    expect(job_2.data).to.deep.equal(jobs[1]);
  });

  it('createPushNotificationsJobs log a message when a job is completed', () => {
    createPushNotificationsJobs(jobs, queue);
    const job = queue.testMode.jobs[0];
    job.emit('complete');
    expect(consoleSpy.calledWithMatch(`Notification job ${job.id} completed`)).to.be.true;
  });
  
  it('createPushNotificationsJobs log a message when a job fails', () => {
    createPushNotificationsJobs(jobs, queue);
    const job = queue.testMode.jobs[0];
    job.emit('failed', new Error('Job failed'));
    expect(consoleSpy.calledWithMatch(`Notification job ${job.id} failed: Job failed`)).to.be.true;
  });
  
  it('createPushNotificationsJobs log a message when a job makes progress', () => {
    createPushNotificationsJobs(jobs, queue);
    const job = queue.testMode.jobs[0];
    job.emit('progress', 100);
    expect(consoleSpy.calledWithMatch(`Notification job ${job.id} 100% complete`)).to.be.true;
  });
});
